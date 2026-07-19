<?php
/**
 * Plugin Name: AI COS Connector
 * Plugin URI: https://aspirantveda.in
 * Description: AI COS WordPress connector plugin.
 * Version: 1.0.0
 * Author: Pawan Gayari
 * License: GPL2
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Plugin constants
 */
define(
    'AICOS_VERSION',
    '1.0.0'
);

define(
    'AICOS_PLUGIN_PATH',
    plugin_dir_path(__FILE__)
);

define(
    'AICOS_PLUGIN_URL',
    plugin_dir_url(__FILE__)
);

/**
 * Load required files
 */
require_once AICOS_PLUGIN_PATH .
    'includes/class-auth.php';

require_once AICOS_PLUGIN_PATH .
    'includes/class-posts.php';

require_once AICOS_PLUGIN_PATH .
    'includes/class-api.php';

require_once AICOS_PLUGIN_PATH .
    'includes/class-settings.php';

/**
 * Main plugin class
 */
class AICOSConnector
{
    /**
     * Constructor
     */
    public function __construct()
    {
        $this->init_hooks();
    }

    /**
     * Initialize plugin hooks
     */
    private function init_hooks(): void
    {
        add_action(

            'plugins_loaded',

            [$this, 'boot']
        );
    }

    /**
     * Boot plugin services
     */
    public function boot(): void
    {
        new AICOSAuth();

        new AICOSPosts();

        new AICOSAPI();

        new AICOSSettings();
    }
}

/**
 * Start plugin
 */
new AICOSConnector();