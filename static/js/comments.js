// comments.js - AJAX handling for comments and votes

// Prevent multiple initializations (in case script is loaded twice)
if (window._commentsJsInitialized) {
    console.warn('comments.js already initialized, skipping duplicate init');
} else {
    window._commentsJsInitialized = true;
    document.addEventListener('DOMContentLoaded', function () {
        initCommentInteractions();
    });
}

function initCommentInteractions() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    // 1. Handle Comment/Reply Submissions
    // specific to buttons with type="submit" inside .comment-form
    document.body.addEventListener('click', async function (e) {
        const btn = e.target.closest('button[type="submit"]');
        if (!btn) return;

        const form = btn.closest('.comment-form');
        if (!form) return;

        // Prevent double submission
        if (form.dataset.submitting === 'true') {
            e.preventDefault();
            return;
        }

        e.preventDefault(); // Stop standard form submit
        form.dataset.submitting = 'true'; // Mark as submitting

        const formData = new FormData(form);
        const actionUrl = form.action;

        // Visual feedback
        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Posting...';

        try {
            const response = await fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();

            if (data.success) {
                // Determine insertion point
                // If this was a top-level post comment
                if (form.closest('.post-create-card')) {
                    // This is top level
                    // Wait, usually the form is in the comments section
                    // For tree hole, the form is at the top of comments list usually
                }

                // Find container to append to
                // For a reply, it's usually adjacent. 
                // For a new comment on post, it's the specific list.

                // If reply:
                const replyContainer = form.closest('.reply-form-container');
                if (replyContainer) {
                    // It's a reply
                    // Insert before the reply form or at the end of siblings?
                    // Usually we replace the form or append to the children list.
                    // Let's assume standard structure: .comment-item -> .replies
                    // But for now, we can reload or just show toast?
                    // The view returns 'html'.

                    // Simple approach: show toast, reload or insert if simple
                    if (data.html) {
                        // Insert the new comment HTML
                        // If invalid html structure, might be tricky. 
                        // Assuming data.html is the <li>...</li>

                        // If it is a reply
                        const parentComment = replyContainer.closest('.comment-item');
                        if (parentComment) {
                            let repliesList = parentComment.querySelector('.replies-list');
                            if (!repliesList) {
                                repliesList = document.createElement('ul');
                                repliesList.className = 'replies-list';
                                parentComment.appendChild(repliesList);
                            }
                            repliesList.insertAdjacentHTML('beforeend', data.html);

                            // Hide form
                            replyContainer.style.display = 'none';
                            form.reset();
                        }
                    }
                } else {
                    // Top level comment
                    const postCard = form.closest('.post-card');
                    if (postCard) {
                        const commentsList = postCard.querySelector('.comments-list');
                        if (commentsList) {
                            // Check if empty state exists and remove it
                            const emptyState = commentsList.querySelector('.no-comments');
                            if (emptyState) emptyState.remove();

                            commentsList.insertAdjacentHTML('beforeend', data.html);
                            form.reset();
                        }
                    }
                }

                showToast(data.message || 'Comment posted!', 'success');

                // Update count if present
                if (data.comment_count !== undefined) {
                    const countBadge = form.closest('.post-card')?.querySelector('.comment-pill .pill-label');
                    if (countBadge) countBadge.textContent = data.comment_count;
                }

            } else {
                showToast(data.message || 'Error posting comment', 'error');
            }

        } catch (error) {
            console.error('Error:', error);
            showToast('Network error. Please try again.', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalText;
            form.dataset.submitting = 'false'; // Reset submission flag
        }
    });

    // 2. Handle Upvote/Downvote/Flag/Delete Buttons (AJAX)
    document.body.addEventListener('click', async function (e) {
        const btn = e.target.closest('.vote-btn, .action-pill.flag-pill');
        // Note: delete button might be different class. 
        // Let's handle votes primarily.

        if (!btn) return;

        // If it's a flag button form submit, prevent default and do ajax
        // If it's a vote button (not a form, just button with data attributes usually, OR form)
        // Check HTML: Vote buttons are buttons. Flag is form > button.

        if (btn.classList.contains('vote-btn')) {
            handleVoteCheck(e, btn, csrfToken);
        } else if (btn.classList.contains('flag-pill') && btn.type === 'submit') {
            // Handle flag form
            e.preventDefault();
            handleFormAction(btn.form, csrfToken);
        }
    });
}

async function handleVoteCheck(e, btn, csrfToken) {
    // Prevent default just in case
    e.preventDefault();

    // If it's a comment vote vs post vote
    // HTML for comment vote: <form action="..."> <button type="submit" ...>
    // HTML for post vote: <button data-post-id="..."> (handled in home.js usually?)
    // Let's check if it is inside .comment-item

    if (btn.closest('.comment-item')) {
        // It is a comment vote
        const form = btn.closest('form');
        if (form) {
            handleFormAction(form, csrfToken, (data) => {
                // Update UI
                // data should contain new score variables
                // But wait, the view returns generic success usually?
                // Let's assume the view returns net_score.

                const scoreSpan = form.parentElement.querySelector('.vote-score');
                if (scoreSpan && data.net_score !== undefined) {
                    scoreSpan.textContent = data.net_score;
                }

                // Toggle active class
                // Reset all buttons in this group
                form.parentElement.querySelectorAll('.vote-btn').forEach(b => b.classList.remove('active'));

                if (data.user_vote_type === 'UPVOTE' && btn.classList.contains('upvote')) {
                    btn.classList.add('active');
                } else if (data.user_vote_type === 'DOWNVOTE' && btn.classList.contains('downvote')) {
                    btn.classList.add('active');
                }
            });
        }
    } else {
        // Post vote (handled by home.js usually, but let's double check conflicts)
        // If home.js handles it, we should let it bubble or ignore?
        // home.js usually handles .vote-btn on posts.
        // We should skip if not comment.
    }
}

async function handleFormAction(form, csrfToken, successCallback) {
    const actionUrl = form.action;

    try {
        const response = await fetch(actionUrl, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            body: new FormData(form)
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            if (successCallback) successCallback(data);
        } else {
            showToast(data.message || 'Action failed', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Connection error', 'error');
    }
}
