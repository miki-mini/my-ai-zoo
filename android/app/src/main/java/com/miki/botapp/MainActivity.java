package com.miki.botapp;

import com.getcapacitor.BridgeActivity;

/**
 * MainActivity — Capacitor Bridge Entry Point
 *
 * SOURCE: https://capacitorjs.com/docs/android
 * "MainActivity extends BridgeActivity, which is Capacitor's Android Activity.
 * Custom plugins are registered here so the JavaScript bridge can call them
 * via window.Capacitor.Plugins.<PluginName>."
 *
 * BernardBeaconPlugin is registered to expose:
 *   - getLocation()         GPS coordinates via FusedLocationProviderClient
 *   - copyToClipboard()     Writes text to system clipboard
 *   - openHotspotSettings() Intent to Android tethering settings panel
 *   - startServer()         Launches NanoHTTPD captive portal server
 *   - stopServer()          Stops the HTTP server
 *   - isServerRunning()     Returns server liveness status
 *   - getHotspotInfo()      Returns current device IP on hotspot network
 */
public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(android.os.Bundle savedInstanceState) {
        // Register custom plugins BEFORE super.onCreate() so Capacitor's
        // JavaScript bridge initialises with them available.
        registerPlugin(BernardBeaconPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
