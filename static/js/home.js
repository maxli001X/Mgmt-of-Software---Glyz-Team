// Tree Hole Yale - Home Page JavaScript
// All functionality for the home feed page

(function() {
    'use strict';

    // ================== Search Functionality ==================
    function initSearchFunctionality() {
        const searchInput = document.getElementById('search-input');
        const searchForm = document.querySelector('.search-form');
        const searchWrapper = document.querySelector('.search-wrapper');
        let debounceTimer;
        let suggestionsContainer = null;

        if (searchInput && searchForm) {
            // Create suggestions dropdown
            suggestionsContainer = document.createElement('div');
            suggestionsContainer.className = 'search-suggestions';
            suggestionsContainer.style.display = 'none';
            searchWrapper.style.position = 'relative';
            searchWrapper.appendChild(suggestionsContainer);

            // Fetch suggestions from API
            async function fetchSearchSuggestions(query) {
                if (query.length < 2) {
                    suggestionsContainer.style.display = 'none';
                    return;
                }

                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                
                try {
                    const response = await fetch(`/api/search-suggestions/?q=${encodeURIComponent(query)}`, {
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    if (response.ok) {
                        const data = await response.json();
                        displaySearchSuggestions(data);
                    }
                } catch (error) {
                    console.log('Search suggestions failed:', error);
                }
            }

            function displaySearchSuggestions(data) {
                if ((!data.tags || data.tags.length === 0) && (!data.recent_posts || data.recent_posts.length === 0)) {
                    suggestionsContainer.style.display = 'none';
                    return;
                }

                let html = '';

                if (data.tags && data.tags.length > 0) {
                    html += '<div class="suggestions-section"><div class="suggestions-header">Tags</div>';
                    data.tags.forEach(tag => {
                        html += `<a href="?tag=${encodeURIComponent(tag.name)}" class="suggestion-item tag-suggestion">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                                <line x1="7" y1="7" x2="7.01" y2="7"></line>
                            </svg>
                            <span>${tag.name}</span>
                            <span class="suggestion-count">${tag.count}</span>
                        </a>`;
                    });
                    html += '</div>';
                }

                if (data.recent_posts && data.recent_posts.length > 0) {
                    html += '<div class="suggestions-section"><div class="suggestions-header">Recent Posts</div>';
                    data.recent_posts.forEach(post => {
                        html += `<a href="?q=${encodeURIComponent(post.title)}" class="suggestion-item post-suggestion">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                            </svg>
                            <span>${post.title}</span>
                        </a>`;
                    });
                    html += '</div>';
                }

                suggestionsContainer.innerHTML = html;
                suggestionsContainer.style.display = 'block';
            }

            // Auto-submit on input with debounce (500ms delay)
            searchInput.addEventListener('input', function () {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(function () {
                    const query = searchInput.value.trim();
                    
                    // Show suggestions if 2+ chars
                    if (query.length >= 2) {
                        fetchSearchSuggestions(query);
                    } else {
                        suggestionsContainer.style.display = 'none';
                    }

                    // Auto-submit if 3+ chars or clearing
                    if (query.length >= 3 || query.length === 0) {
                        searchForm.submit();
                    }
                }, 500);
            });

            // Submit on Enter key
            searchInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    clearTimeout(debounceTimer);
                    suggestionsContainer.style.display = 'none';
                    searchForm.submit();
                } else if (e.key === 'Escape') {
                    suggestionsContainer.style.display = 'none';
                }
            });

            // Hide suggestions on focus out
            searchInput.addEventListener('blur', function() {
                setTimeout(() => {
                    suggestionsContainer.style.display = 'none';
                }, 200);
            });

            // Show suggestions on focus if there's a query
            searchInput.addEventListener('focus', function() {
                if (searchInput.value.length >= 2) {
                    fetchSearchSuggestions(searchInput.value);
                }
            });
        }
    }

    // ================== Hashtag Detection ==================
    function initHashtagDetection() {
        const bodyTextarea = document.getElementById('id_body');
        const hashtagPreview = document.getElementById('hashtag-preview');
        const hashtagList = document.getElementById('hashtag-list');

        if (bodyTextarea && hashtagPreview && hashtagList) {
            function extractHashtags(text) {
                if (!text) return [];
                const hashtagPattern = /#([a-zA-Z0-9_-]+)/g;
                const matches = [];
                let match;

                while ((match = hashtagPattern.exec(text)) !== null) {
                    const tag = match[1].toLowerCase().trim();
                    if (tag && tag.length >= 2 && tag.length <= 50 && !matches.includes(tag)) {
                        matches.push(tag);
                    }
                }

                return matches;
            }

            function updateHashtagPreview() {
                const text = bodyTextarea.value;
                const hashtags = extractHashtags(text);

                if (hashtags.length > 0) {
                    hashtagList.innerHTML = hashtags.map(tag =>
                        '<span class="hashtag-badge">#' + tag + '</span>'
                    ).join('');
                    hashtagPreview.style.display = 'block';
                } else {
                    hashtagPreview.style.display = 'none';
                }
            }

            bodyTextarea.addEventListener('input', updateHashtagPreview);
            bodyTextarea.addEventListener('paste', function () {
                setTimeout(updateHashtagPreview, 10);
            });

            updateHashtagPreview();
        }
    }

    // ================== Identity State Management ==================
    function updateIdentityState(value) {
        const isAnonymousCheckbox = document.getElementById('id_is_anonymous');

        if (value === 'anonymous') {
            if (isAnonymousCheckbox) isAnonymousCheckbox.checked = true;
        } else {
            if (isAnonymousCheckbox) isAnonymousCheckbox.checked = false;
        }
    }

    function initIdentityState() {
        updateIdentityState('anonymous');
    }

    // Make updateIdentityState globally available for inline handlers
    window.updateIdentityState = updateIdentityState;

    // ================== AI Tag Suggestions ==================
    function initAITagSuggestions(suggestTagsUrl) {
        const titleInput = document.getElementById('id_title');
        const bodyTextarea = document.getElementById('id_body');
        const tagsInput = document.getElementById('id_tags_input');

        if (!titleInput || !bodyTextarea || !tagsInput) return;

        const suggestContainer = document.createElement('div');
        suggestContainer.id = 'tag-suggestions';
        suggestContainer.className = 'tag-suggestions';
        suggestContainer.style.display = 'none';
        suggestContainer.innerHTML = '<span class="suggestion-label">Suggested tags:</span><span class="suggestion-chips"></span>';
        tagsInput.parentNode.insertBefore(suggestContainer, tagsInput.nextSibling);

        let suggestTimeout;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

        async function fetchSuggestions() {
            const title = titleInput.value.trim();
            const body = bodyTextarea.value.trim();

            if (title.length + body.length < 20) {
                suggestContainer.style.display = 'none';
                return;
            }

            try {
                const response = await fetch(suggestTagsUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ title, body })
                });

                if (response.ok) {
                    const data = await response.json();
                    displaySuggestions(data.tags);
                }
            } catch (error) {
                console.log('Tag suggestion request failed');
            }
        }

        function displaySuggestions(tags) {
            const chipsContainer = suggestContainer.querySelector('.suggestion-chips');

            if (!tags || tags.length === 0) {
                suggestContainer.style.display = 'none';
                return;
            }

            const currentTags = tagsInput.value.toLowerCase().split(',').map(t => t.trim());
            const filteredTags = tags.filter(tag =>
                !currentTags.includes(tag.toLowerCase())
            );

            if (filteredTags.length === 0) {
                suggestContainer.style.display = 'none';
                return;
            }

            chipsContainer.innerHTML = filteredTags.map(tag =>
                '<button type="button" class="suggestion-chip" data-tag="' + tag + '">' + tag + '</button>'
            ).join('');

            suggestContainer.style.display = 'block';

            chipsContainer.querySelectorAll('.suggestion-chip').forEach(chip => {
                chip.addEventListener('click', function () {
                    const tag = this.dataset.tag;
                    const current = tagsInput.value.trim();
                    if (current) {
                        tagsInput.value = current + ', ' + tag;
                    } else {
                        tagsInput.value = tag;
                    }
                    this.remove();
                    if (chipsContainer.children.length === 0) {
                        suggestContainer.style.display = 'none';
                    }
                });
            });
        }

        function debouncedFetch() {
            clearTimeout(suggestTimeout);
            suggestTimeout = setTimeout(fetchSuggestions, 800);
        }

        titleInput.addEventListener('input', debouncedFetch);
        bodyTextarea.addEventListener('input', debouncedFetch);
    }

    // ================== Post Collapse ==================
    function initPostCollapse() {
        const WORD_LIMIT = 250;
        const posts = document.querySelectorAll('.post-body-content');

        posts.forEach(post => {
            const text = post.innerText;
            const wordCount = text.trim().split(/\s+/).length;

            if (wordCount > WORD_LIMIT) {
                const readMoreBtn = document.createElement('button');
                readMoreBtn.className = 'read-more-btn';
                readMoreBtn.innerText = 'Read more';
                readMoreBtn.onclick = function () {
                    post.classList.remove('collapsed');
                    readMoreBtn.style.display = 'none';
                };

                post.classList.add('collapsed');
                post.parentNode.insertBefore(readMoreBtn, post.nextSibling);
            }
        });
    }

    // ================== FAB Visibility ==================
    function initFABVisibility() {
        const fab = document.getElementById('fab-share-thought');
        const postFormSection = document.getElementById('create-post-section');

        if (!fab || !postFormSection) return;

        function checkFabVisibility() {
            const rect = postFormSection.getBoundingClientRect();
            if (rect.bottom < 0) {
                fab.classList.add('visible');
            } else {
                fab.classList.remove('visible');
            }
        }

        window.addEventListener('scroll', checkFabVisibility);
        checkFabVisibility();
    }

    // ================== Modal Logic ==================
    function initModalLogic() {
        const postForm = document.getElementById('post-form');
        const staticContainer = document.getElementById('post-form-content');
        const modalContainer = document.getElementById('modal-form-container');
        const modal = document.getElementById('post-modal');

        window.openPostModal = function() {
            if (!postForm || !modalContainer) return;
            modalContainer.appendChild(postForm);
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        };

        window.closePostModal = function() {
            if (!postForm || !staticContainer) return;
            staticContainer.appendChild(postForm);
            modal.style.display = 'none';
            document.body.style.overflow = '';
        };

        if (modal) {
            window.onclick = function (event) {
                if (event.target == modal) {
                    window.closePostModal();
                }
            };
        }
    }

    // ================== Vote Handling ==================
    async function handleVote(postId, voteType) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (!csrfToken) {
            alert('Please log in to vote.');
            return;
        }

        const url = `/posts/${postId}/${voteType}vote/`;

        // Add loading state
        const voteButtons = document.querySelectorAll(`[data-post-id="${postId}"] .vote-button`);
        voteButtons.forEach(btn => {
            btn.classList.add('loading');
            btn.disabled = true;
        });

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                if (response.status === 403) {
                    alert('Please log in to vote.');
                    window.location.href = '/auth/login/';
                } else {
                    alert('Vote failed. Please try again.');
                }
                return;
            }

            const data = await response.json();

            if (data.success) {
                const voteCountSpan = document.getElementById(`vote-count-${postId}`);
                if (voteCountSpan) {
                    voteCountSpan.textContent = data.net_votes;
                    voteCountSpan.classList.remove('positive', 'negative');
                    if (data.net_votes > 0) voteCountSpan.classList.add('positive');
                    else if (data.net_votes < 0) voteCountSpan.classList.add('negative');
                }

                const postCard = document.querySelector(`.post-card[data-post-id="${postId}"]`);
                if (postCard) {
                    const upvoteBtn = postCard.querySelector('.upvote-button');
                    const downvoteBtn = postCard.querySelector('.downvote-button');

                    if (upvoteBtn) upvoteBtn.classList.remove('active');
                    if (downvoteBtn) downvoteBtn.classList.remove('active');

                    if (data.user_vote === 'UPVOTE') {
                        if (upvoteBtn) upvoteBtn.classList.add('active');
                    } else if (data.user_vote === 'DOWNVOTE') {
                        if (downvoteBtn) downvoteBtn.classList.add('active');
                    }
                }
            } else {
                alert(data.message || 'Vote failed.');
            }
        } catch (error) {
            console.error('Network error:', error);
            alert('Network error. Please try again.');
        } finally {
            // Remove loading state
            voteButtons.forEach(btn => {
                btn.classList.remove('loading');
                btn.disabled = false;
            });
        }
    }

    window.handleVote = handleVote;

    // ================== Flag Forms ==================
    function initFlagForms() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        document.querySelectorAll('.flag-form').forEach(form => {
            form.addEventListener('submit', async function (e) {
                e.preventDefault();
                const url = this.action;
                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    const data = await response.json();
                    if (data.success) {
                        alert(data.message);
                    } else {
                        alert(data.message || 'Already flagged');
                    }
                } catch (error) {
                    console.error('Network error:', error);
                }
            });
        });
    }

    // ================== Scroll to Post Form ==================
    function scrollToPostForm() {
        const createPostSection = document.getElementById('create-post-section');
        if (createPostSection) {
            createPostSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            setTimeout(() => {
                const titleInput = document.getElementById('id_title');
                if (titleInput) titleInput.focus();
            }, 500);
        }
    }

    window.scrollToPostForm = scrollToPostForm;

    // ================== Toggle Comments ==================
    function toggleComments(postId) {
        const commentsWrapper = document.getElementById(`comments-wrapper-${postId}`);
        const btn = document.querySelector(`[data-post-id="${postId}"] .header-reply-button`);

        if (commentsWrapper) {
            const isHidden = commentsWrapper.style.display === 'none';
            commentsWrapper.style.display = isHidden ? 'block' : 'none';

            if (btn) {
                btn.classList.toggle('active', isHidden);
            }
        }
    }

    window.togglePostComments = toggleComments;

    // ================== Auto-scroll to Posts Section ==================
    function initAutoScroll() {
        if (window.location.hash === '#posts-section') {
            setTimeout(() => {
                const postsSection = document.getElementById('posts-section');
                if (postsSection) {
                    postsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);
        }
    }

    // ================== Initialization ==================
    document.addEventListener('DOMContentLoaded', function() {
        initSearchFunctionality();
        initHashtagDetection();
        initIdentityState();
        initPostCollapse();
        initFABVisibility();
        initModalLogic();
        initFlagForms();
        initAutoScroll();

        // AI Tag Suggestions needs URL from template
        const suggestTagsUrl = document.querySelector('[data-suggest-tags-url]')?.dataset.suggestTagsUrl;
        if (suggestTagsUrl) {
            initAITagSuggestions(suggestTagsUrl);
        }
    });

})();

