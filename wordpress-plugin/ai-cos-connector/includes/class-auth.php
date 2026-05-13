<?php

if (!defined('ABSPATH')) {
    exit;
}

/**
 * AI COS Authentication
 */
class AICOSAuth
{
    /**
     * Option key
     */
    private string $option_key =
        'aicos_api_key';

    /**
     * Constructor
     */
    public function __construct()
    {
        add_action(

            'admin_init',

            [$this, 'generate_api_key']
        );
    }

    /**
     * Generate API key
     */
    public function generate_api_key(): void
    {
        $existing_key = get_option(
            $this->option_key
        );

        if (!empty($existing_key)) {
            return;
        }

        $api_key = wp_generate_password(

            64,

            false,

            false
        );

        update_option(

            $this->option_key,

            $api_key
        );
    }

    /**
     * Get API key
     */
    public function get_api_key(): string
    {
        return (string) get_option(
            $this->option_key,
            ''
        );
    }

    /**
     * Validate API request
     */
    public function validate_request(
        WP_REST_Request $request
    ): bool {

        $provided_key = $request->get_header(
            'X-AICOS-KEY'
        );

        if (empty($provided_key)) {

            return false;
        }

        $saved_key = $this->get_api_key();

        if (empty($saved_key)) {

            return false;
        }

        return hash_equals(

            $saved_key,

            $provided_key
        );
    }

    /**
     * Unauthorized response
     */
    public function unauthorized_response()
    {
        return new WP_REST_Response(

            [
                'success' => false,

                'error' => (
                    'Unauthorized request.'
                ),
            ],

            401
        );
    }
}