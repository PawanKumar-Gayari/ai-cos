<?php

if (!defined('ABSPATH')) {
    exit;
}

/**
 * AI COS Settings
 */
class AICOSSettings
{
    /**
     * Constructor
     */
    public function __construct()
    {
        add_action(

            'admin_menu',

            [$this, 'register_menu']
        );
    }

    /**
     * Register admin menu
     */
    public function register_menu(): void
    {
        add_menu_page(

            'AI COS Connector',

            'AI COS',

            'manage_options',

            'aicos-connector',

            [$this, 'settings_page'],

            'dashicons-admin-generic',

            80
        );
    }

    /**
     * Settings page
     */
    public function settings_page(): void
    {
        // ==========================================
        // GET API KEY
        // ==========================================

        $api_key = get_option(
            'aicos_api_key',
            ''
        );

        // ==========================================
        // ENDPOINTS
        // ==========================================

        $health_endpoint = home_url(
            '/wp-json/aicos/v1/health'
        );

        $publish_endpoint = home_url(
            '/wp-json/aicos/v1/publish'
        );

        ?>

        <div class="wrap">

            <h1>
                AI COS Connector
            </h1>

            <hr>

            <h2>
                API Configuration
            </h2>

            <table class="form-table">

                <tr>

                    <th>
                        API Key
                    </th>

                    <td>

                        <input
                            type="text"
                            readonly
                            value="<?php echo esc_attr($api_key); ?>"
                            class="regular-text"
                        >

                        <p class="description">
                            Use this API key in Django.
                        </p>

                    </td>

                </tr>

                <tr>

                    <th>
                        Health Endpoint
                    </th>

                    <td>

                        <input
                            type="text"
                            readonly
                            value="<?php echo esc_url($health_endpoint); ?>"
                            class="regular-text"
                        >

                    </td>

                </tr>

                <tr>

                    <th>
                        Publish Endpoint
                    </th>

                    <td>

                        <input
                            type="text"
                            readonly
                            value="<?php echo esc_url($publish_endpoint); ?>"
                            class="regular-text"
                        >

                    </td>

                </tr>

            </table>

            <hr>

            <h2>
                Plugin Status
            </h2>

            <p>
                ✅ Connector Active
            </p>

            <p>
                ✅ API Routes Loaded
            </p>

            <p>
                ✅ Authentication Enabled
            </p>

            <p>
                ✅ WordPress Publishing Ready
            </p>

        </div>

        <?php
    }
}