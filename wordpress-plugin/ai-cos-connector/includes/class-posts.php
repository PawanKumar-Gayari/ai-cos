<?php

if (!defined('ABSPATH')) {
    exit;
}

/**
 * AI COS Post Manager
 */
class AICOSPosts
{
    /**
     * Create WordPress post
     */
    public function create_post(
        array $data
    ): array {

        try {

            // ======================================
            // EXTRACT DATA
            // ======================================

            $title = $data['title'] ?? '';

            $content = $data['content'] ?? '';

            $excerpt = $data['excerpt'] ?? '';

            $status = $data['status'] ?? 'draft';

            // ======================================
            // VALIDATE
            // ======================================

            if (empty($title)) {

                return [

                    'success' => false,

                    'error' => (
                        'Post title is required.'
                    ),
                ];
            }

            if (empty($content)) {

                return [

                    'success' => false,

                    'error' => (
                        'Post content is required.'
                    ),
                ];
            }

            // ======================================
            // PREPARE POST DATA
            // ======================================

            $post_data = [

                'post_title' => $title,

                'post_content' => $content,

                'post_excerpt' => $excerpt,

                'post_status' => $status,

                'post_type' => 'post',
            ];

            // ======================================
            // INSERT POST
            // ======================================

            $post_id = wp_insert_post(

                $post_data,

                true
            );

            // ======================================
            // HANDLE ERRORS
            // ======================================

            if (is_wp_error($post_id)) {

                return [

                    'success' => false,

                    'error' => (
                        $post_id->get_error_message()
                    ),
                ];
            }

            // ======================================
            // GET POST URL
            // ======================================

            $url = get_permalink(
                $post_id
            );

            // ======================================
            // RESPONSE
            // ======================================

            return [

                'success' => true,

                'post_id' => $post_id,

                'url' => $url,

                'status' => get_post_status(
                    $post_id
                ),

                'message' => (
                    'Post created successfully.'
                ),
            ];

        } catch (Exception $error) {

            return [

                'success' => false,

                'error' => (
                    $error->getMessage()
                ),
            ];
        }
    }

    /**
     * Update existing post
     */
    public function update_post(
        int $post_id,
        array $data
    ): array {

        try {

            // ======================================
            // VALIDATE POST
            // ======================================

            if (!get_post($post_id)) {

                return [

                    'success' => false,

                    'error' => (
                        'Post not found.'
                    ),
                ];
            }

            // ======================================
            // UPDATE DATA
            // ======================================

            $update_data = [

                'ID' => $post_id,
            ];

            if (!empty($data['title'])) {

                $update_data[
                    'post_title'
                ] = $data['title'];
            }

            if (!empty($data['content'])) {

                $update_data[
                    'post_content'
                ] = $data['content'];
            }

            if (!empty($data['excerpt'])) {

                $update_data[
                    'post_excerpt'
                ] = $data['excerpt'];
            }

            if (!empty($data['status'])) {

                $update_data[
                    'post_status'
                ] = $data['status'];
            }

            // ======================================
            // UPDATE POST
            // ======================================

            $result = wp_update_post(

                $update_data,

                true
            );

            // ======================================
            // HANDLE ERRORS
            // ======================================

            if (is_wp_error($result)) {

                return [

                    'success' => false,

                    'error' => (
                        $result->get_error_message()
                    ),
                ];
            }

            return [

                'success' => true,

                'post_id' => $post_id,

                'url' => get_permalink(
                    $post_id
                ),

                'status' => get_post_status(
                    $post_id
                ),

                'message' => (
                    'Post updated successfully.'
                ),
            ];

        } catch (Exception $error) {

            return [

                'success' => false,

                'error' => (
                    $error->getMessage()
                ),
            ];
        }
    }

    /**
     * Get post
     */
    public function get_post(
        int $post_id
    ): array {

        $post = get_post(
            $post_id
        );

        if (!$post) {

            return [

                'success' => false,

                'error' => (
                    'Post not found.'
                ),
            ];
        }

        return [

            'success' => true,

            'post_id' => $post->ID,

            'title' => (
                $post->post_title
            ),

            'content' => (
                $post->post_content
            ),

            'status' => (
                $post->post_status
            ),

            'url' => get_permalink(
                $post->ID
            ),
        ];
    }
}