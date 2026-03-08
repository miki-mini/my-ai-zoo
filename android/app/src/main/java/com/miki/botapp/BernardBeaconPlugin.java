package com.miki.botapp;

import android.Manifest;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.net.wifi.WifiManager;
import android.provider.Settings;

import androidx.core.app.ActivityCompat;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.Priority;
import com.google.android.gms.tasks.CancellationTokenSource;

/**
 * BernardBeaconPlugin — Capacitor Native Bridge
 *
 * Exposes Android system APIs to the JavaScript web layer.
 * Registered in MainActivity so Capacitor's JS runtime can call methods
 * via window.Capacitor.Plugins.BernardBeacon.methodName({...}).
 *
 * SOURCE: https://capacitorjs.com/docs/plugins/android
 * "Android Capacitor plugins extend the Plugin class and use @CapacitorPlugin
 * and @PluginMethod annotations to expose methods to JavaScript."
 */
@CapacitorPlugin(
    name = "BernardBeacon",
    permissions = {
        @Permission(
            alias = "location",
            strings = {
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION
            }
        )
    }
)
public class BernardBeaconPlugin extends Plugin {

    private SOSHttpServer httpServer;
    private FusedLocationProviderClient fusedClient;
    private PluginCall savedLocationCall;

    @Override
    public void load() {
        // SOURCE: https://developers.google.com/android/reference/com/google/android/gms/location/FusedLocationProviderClient
        // "The main entry point for interacting with the fused location provider.
        // The fused location provider manages the underlying location technology
        // and provides a simple API, conserving battery power." — Chosen over
        // android.location.LocationManager because it automatically selects
        // the best provider (GPS, Wi-Fi, Cell) and handles duty-cycling.
        fusedClient = LocationServices.getFusedLocationProviderClient(getActivity());
    }

    // ══════════════════════════════════════════════════════════════════
    // GPS LOCATION
    //
    // SOURCE: https://developer.android.com/training/location/retrieve-current
    // "To get the precise location of a device, you can use the
    // FusedLocationProviderClient." — getCurrentLocation() returns a one-shot
    // high-accuracy fix, then immediately stops the sensor to conserve battery.
    // ══════════════════════════════════════════════════════════════════

    @PluginMethod
    public void getLocation(PluginCall call) {
        if (ActivityCompat.checkSelfPermission(getContext(),
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            savedLocationCall = call;
            requestPermissionForAlias("location", call, "locationPermCallback");
            return;
        }
        fetchLocation(call);
    }

    @PermissionCallback
    private void locationPermCallback(PluginCall call) {
        if (ActivityCompat.checkSelfPermission(getContext(),
                Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            fetchLocation(call);
        } else {
            call.reject("位置情報の許可が拒否されました");
        }
    }

    private void fetchLocation(PluginCall call) {
        CancellationTokenSource cts = new CancellationTokenSource();
        fusedClient.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, cts.getToken())
            .addOnSuccessListener(location -> {
                if (location == null) {
                    call.reject("位置情報を取得できませんでした");
                    return;
                }
                JSObject ret = new JSObject();
                ret.put("lat",      location.getLatitude());
                ret.put("lng",      location.getLongitude());
                ret.put("accuracy", location.getAccuracy());
                call.resolve(ret);
            })
            .addOnFailureListener(e -> call.reject("GPS エラー: " + e.getMessage()));
    }

    // ══════════════════════════════════════════════════════════════════
    // CLIPBOARD
    //
    // SOURCE: https://developer.android.com/reference/android/content/ClipboardManager
    // "Interface to the clipboard service, for placing and retrieving text in
    // the global clipboard." — Allows the user to paste the generated SOS SSID
    // directly into the Android Hotspot settings name field without typos,
    // critical under stress conditions.
    // ══════════════════════════════════════════════════════════════════

    @PluginMethod
    public void copyToClipboard(PluginCall call) {
        String text = call.getString("text", "");
        ClipboardManager cm =
            (ClipboardManager) getContext().getSystemService(Context.CLIPBOARD_SERVICE);
        cm.setPrimaryClip(ClipData.newPlainText("SOS SSID", text));

        JSObject ret = new JSObject();
        ret.put("success", true);
        call.resolve(ret);
    }

    // ══════════════════════════════════════════════════════════════════
    // OPEN HOTSPOT SETTINGS
    //
    // SOURCE: https://developer.android.com/reference/android/provider/Settings#ACTION_WIRELESS_SETTINGS
    // "Activity Action: Show settings to allow configuration of wireless
    // controls such as Wi-Fi, Bluetooth and Mobile networks."
    //
    // Why not set the SSID programmatically?
    // Android 10 (API 29) deprecated WifiManager.setWifiApConfiguration():
    // SOURCE: https://developer.android.com/reference/android/net/wifi/WifiManager#setWifiApConfiguration(android.net.wifi.WifiConfiguration)
    // "This method was deprecated in API level 29." — Apps can no longer change
    // hotspot SSIDs without OVERRIDE_WIFI_CONFIG (a system-only permission).
    // Instead, we copy the SSID to clipboard and open the settings panel,
    // guiding the user to paste it manually — a "semi-automated" approach.
    // ══════════════════════════════════════════════════════════════════

    @PluginMethod
    public void openHotspotSettings(PluginCall call) {
        try {
            // Attempt direct route to Tethering & portable hotspot screen
            Intent intent = new Intent();
            intent.setClassName(
                "com.android.settings",
                "com.android.settings.TetherSettings"
            );
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(intent);
            call.resolve();
        } catch (Exception e) {
            try {
                // Fallback: Android 10+ Settings Panel for Wi-Fi
                // SOURCE: https://developer.android.com/reference/android/provider/Settings.Panel
                Intent panel = new Intent(Settings.Panel.ACTION_INTERNET_CONNECTIVITY);
                panel.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getContext().startActivity(panel);
                call.resolve();
            } catch (Exception e2) {
                // Last resort: general wireless settings
                Intent fallback = new Intent(Settings.ACTION_WIRELESS_SETTINGS);
                fallback.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getContext().startActivity(fallback);
                call.resolve();
            }
        }
    }

    // ══════════════════════════════════════════════════════════════════
    // LOCAL HTTP SERVER (Captive Portal)
    //
    // SOURCE: https://github.com/NanoHttpd/nanohttpd
    // "NanoHTTPD is a light-weight HTTP server designed for embedding in
    // other applications." — Serves the SOS rescue page to any device that
    // connects to the Android Wi-Fi hotspot. The server responds to OS-level
    // captive portal probes with a 302 redirect, which automatically prompts
    // connected devices with "Sign in to Wi-Fi network", displaying our page.
    // ══════════════════════════════════════════════════════════════════

    @PluginMethod
    public void startServer(PluginCall call) {
        String html = call.getString("html",
            "<html><body><h1 style='color:red'>SOS</h1></body></html>");
        try {
            if (httpServer != null && httpServer.isAlive()) {
                httpServer.stop();
            }
            httpServer = new SOSHttpServer(html);

            JSObject ret = new JSObject();
            ret.put("success", true);
            ret.put("port",    SOSHttpServer.PORT);
            ret.put("url",     SOSHttpServer.GATEWAY_IP + ":" + SOSHttpServer.PORT);
            call.resolve(ret);
        } catch (Exception e) {
            call.reject("サーバー起動エラー: " + e.getMessage());
        }
    }

    @PluginMethod
    public void stopServer(PluginCall call) {
        if (httpServer != null) {
            httpServer.stop();
            httpServer = null;
        }
        call.resolve();
    }

    @PluginMethod
    public void isServerRunning(PluginCall call) {
        JSObject ret = new JSObject();
        ret.put("running", httpServer != null && httpServer.isAlive());
        call.resolve(ret);
    }

    // ══════════════════════════════════════════════════════════════════
    // WIFI HOTSPOT INFO
    //
    // SOURCE: https://developer.android.com/reference/android/net/wifi/WifiManager
    // "This class provides the primary API for managing all aspects of Wi-Fi
    // connectivity." — Used here in read-only mode to retrieve the current
    // device IP address visible on the hotspot network.
    // ══════════════════════════════════════════════════════════════════

    @PluginMethod
    public void getHotspotInfo(PluginCall call) {
        WifiManager wm =
            (WifiManager) getContext().getApplicationContext()
                .getSystemService(Context.WIFI_SERVICE);

        // getConnectionInfo().getIpAddress() returns an int in little-endian byte order
        int ip = wm.getConnectionInfo().getIpAddress();
        String ipStr = String.format("%d.%d.%d.%d",
            ip & 0xff, (ip >> 8) & 0xff, (ip >> 16) & 0xff, (ip >> 24) & 0xff);

        JSObject ret = new JSObject();
        ret.put("ip",   ipStr);
        ret.put("port", SOSHttpServer.PORT);
        ret.put("url",  "http://" + ipStr + ":" + SOSHttpServer.PORT);
        call.resolve(ret);
    }
}
