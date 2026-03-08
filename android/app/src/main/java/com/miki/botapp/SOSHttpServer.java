package com.miki.botapp;

import java.io.IOException;
import java.util.Map;

import fi.iki.elonen.NanoHTTPD;

/**
 * SOSHttpServer — Captive Portal HTTP Server
 *
 * SOURCE: https://github.com/NanoHttpd/nanohttpd
 * "NanoHTTPD is a light-weight HTTP server designed for embedding in other
 * applications, released under a Modified BSD licence." — Chosen because it
 * requires zero configuration, runs as a single background thread, and has
 * no external dependencies beyond its own JAR.
 *
 * HOW CAPTIVE PORTAL DETECTION WORKS:
 * When a device connects to a Wi-Fi access point with no internet, the OS
 * sends lightweight HTTP probes to well-known URLs. If the response is
 * unexpected (e.g., a 302 redirect instead of 204 No Content), the OS
 * classifies the network as a "captive portal" and presents a
 * "Sign in to network" notification that launches a browser — which then
 * lands on our SOS rescue page.
 *
 * SOURCE: https://developer.android.com/reference/android/net/CaptivePortal
 * "A CaptivePortal object is used to notify the system when a captive portal
 * condition is resolved."
 *
 * LIMITATION (no-root): Port 80 requires root on Linux/Android.
 * This server runs on port 8080. The captive portal probes (port 80) will
 * still trigger "no internet" detection; the rescuer will see a notification
 * and can open any browser URL to reach port 8080 manually.
 * The SSID itself already broadcasts the GPS position — the portal is bonus.
 */
public class SOSHttpServer extends NanoHTTPD {

    public static final int PORT = 8080;
    public static final String GATEWAY_IP = "192.168.43.1"; // Android hotspot default

    private volatile String sosHtml;

    /**
     * Creates and immediately starts the HTTP server.
     *
     * SOURCE: https://github.com/NanoHttpd/nanohttpd#usage
     * "Subclass NanoHTTPD and override serve(). Then call start() to start
     * the server in a background thread."
     */
    public SOSHttpServer(String sosHtml) throws IOException {
        super(PORT);
        this.sosHtml = sosHtml;
        // false = non-daemon thread, so server outlives the calling thread
        start(NanoHTTPD.SOCKET_READ_TIMEOUT, false);
    }

    /** Hot-swap the SOS page content without restarting the server. */
    public void updateContent(String html) {
        this.sosHtml = html;
    }

    /**
     * SOURCE: https://github.com/NanoHttpd/nanohttpd#serving-files
     * "serve(IHTTPSession session) is called for every incoming request.
     * Return a Response object to send back to the client."
     *
     * Request routing:
     *  - Captive portal probes → 302 redirect (triggers OS "Sign in" popup)
     *  - All other requests    → 200 OK with the SOS HTML page
     */
    @Override
    public Response serve(IHTTPSession session) {
        String uri  = session.getUri();
        Map<String, String> headers = session.getHeaders();
        String host = headers.getOrDefault("host", "");

        // ── Detect OS-level captive portal probes ──────────────────
        //
        // SOURCE: https://www.chromium.org/chromium-os/chromiumos-design-docs/network-portal-detection/
        // "Chromium OS network portal detection sends HTTP requests to
        // generate_204 endpoints. A 302 response indicates a captive portal."
        //
        // Known probes by OS:
        //   Android:  GET http://connectivitycheck.gstatic.com/generate_204
        //   Windows:  GET http://www.msftconnecttest.com/connecttest.txt
        //   macOS/iOS: GET http://captive.apple.com/hotspot-detect.html
        boolean isCaptiveProbe =
            uri.contains("generate_204")      ||   // Android / Chrome
            uri.contains("connecttest.txt")   ||   // Windows
            uri.contains("hotspot-detect")    ||   // macOS / iOS
            uri.contains("library/test")      ||   // iOS fallback
            uri.contains("ncsi.txt")          ||   // Windows NCSI
            host.contains("gstatic.com")      ||
            host.contains("apple.com")        ||
            host.contains("msftconnecttest")  ||
            host.contains("msftncsi");

        if (isCaptiveProbe) {
            // Return 302 Found → OS recognises captive portal
            // and presents "Sign in to network" notification
            Response r = newFixedLengthResponse(
                Response.Status.REDIRECT,
                MIME_HTML,
                "<html><body>Redirecting to SOS page...</body></html>"
            );
            r.addHeader("Location", "http://" + GATEWAY_IP + ":" + PORT + "/");
            r.addHeader("Cache-Control", "no-cache, no-store");
            return r;
        }

        // ── Serve SOS rescue page for all other requests ───────────
        Response r = newFixedLengthResponse(
            Response.Status.OK,
            "text/html; charset=utf-8",
            sosHtml
        );
        r.addHeader("Cache-Control", "no-cache, no-store");
        r.addHeader("X-Frame-Options", "DENY");
        return r;
    }
}
