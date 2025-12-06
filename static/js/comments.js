// Tree Hole Yale - Comments JavaScript
// Functionality for comment interactions

(function() {
    'use strict';

    // Toggle reply form visibility
    function toggleReplyForm(commentId) {
        const replyForm = document.getElementById('reply-form-' + commentId);
        if (replyForm) {
            replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
        }
    }

    window.toggleReplyForm = toggleReplyForm;

})();

