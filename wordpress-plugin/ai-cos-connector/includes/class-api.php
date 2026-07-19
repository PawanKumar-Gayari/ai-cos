<?php

if (!defined('ABSPATH')) {
    exit;
}

/**
 * AI COS API Routes
 */
class AICOSAPI
{
    /**
     * API namespace
     */
    private $namespace = 'aicos/v1';

    /**
     * Auth handler
     */
    private $auth;

    /**
     * Posts handler
     */
    private $posts;

    /**
     * Constructor
     */
    public function __construct()
    {
        $this->auth = new AICOSAuth();

        $this->posts = new AICOSPosts();

        add_action(
            'rest_api_init',
            [$this, 'register_routes']
        );
    }

    /**
     * Register routes
     */
    public function register_routes()
    {
        // ==========================================
        // HEALTH ROUTE
        // ==========================================

        register_rest_route(

            $this->namespace,

            '/health',

            [

                'methods' => ['GET'],

                'callback' => [
                    $this,
                    'health_check'
                ],

                'permission_callback' => '__return_true',
            ]
        );

        // ==========================================
        // TEST ROUTE
        // ==========================================

        register_rest_route(

            $this->namespace,

            '/test',

            [

                'methods' => ['GET'],

                'callback' => [
                    $this,
                    'test_route'
                ],

                'permission_callback' => '__return_true',
            ]
        );

        // ==========================================
        // PUBLISH ROUTE
        // ==========================================

        register_rest_route(

            $this->namespace,

            '/publish',

            [

                // DEBUG MODE
                'methods' => ['GET', 'POST'],

                'callback' => [
                    $this,
                    'publish_post'
                ],

                // TEMP DEBUG
                'permission_callback' => '__return_true',
            ]
        );
    }

    /**
     * Health check
     */
    public function health_check()
    {
        return new WP_REST_Response(

            [

                'success' => true,

                'plugin' => (
                    'AI COS Connector'
                ),

                'version' => (
                    AICOS_VERSION
                ),

                'wordpress' => (
                    get_bloginfo(
                        'version'
                    )
                ),

                'site' => home_url(),
            ],

            200
        );
    }

    /**
     * Test route
     */
    public function test_route()
    {
        return new WP_REST_Response(

            [

                'success' => true,

                'message' => (
                    'Test route working.'
                ),
            ],

            200
        );
    }

    /**
     * Publish post
     */
    public function publish_post(
        $request
    ) {

        try {

            // ======================================
            // REQUEST DATA
            // ======================================

            $title = sanitize_text_field(
                $request->get_param(
                    'title'
                )
            );

            $content = wp_kses_post(
                $request->get_param(
                    'content'
                )
            );

            $excerpt = sanitize_text_field(
                $request->get_param(
                    'excerpt'
                )
            );

            $status = sanitize_text_field(
                $request->get_param(
                    'status'
                )
            );

            // ======================================
            // DEFAULT STATUS
            // ======================================

            if (empty($status)) {

                $status = 'draft';
            }

            // ======================================
            // VALIDATION
            // ======================================

            if (empty($title)) {

                return new WP_REST_Response(

                    [

                        'success' => false,

                        'error' => (
                            'Title is required.'
                        ),
                    ],

                    400
                );
            }

            if (empty($content)) {

                return new WP_REST_Response(

                    [

                        'success' => false,

                        'error' => (
                            'Content is required.'
                        ),
                    ],

                    400
                );
            }

            // ======================================
            // CREATE POST
            // ======================================

            $result = $this->posts->create_post(

                [

                    'title' => $title,

                    'content' => $content,

                    'excerpt' => $excerpt,

                    'status' => $status,
                ]
            );

            // ======================================
            // FAILED
            // ======================================

            if (!$result['success']) {

                return new WP_REST_Response(

                    $result,

                    500
                );
            }

            // ======================================
            // SUCCESS
            // ======================================

            return new WP_REST_Response(

                $result,

                200
            );

        } catch (Exception $error) {

            return new WP_REST_Response(

                [

                    'success' => false,

                    'error' => (
                        $error->getMessage()
                    ),
                ],

                500
            );
        }
    }
}