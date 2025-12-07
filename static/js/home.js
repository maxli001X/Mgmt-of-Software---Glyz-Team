// Tree Hole Yale - Home Page JavaScript
// All functionality for the home feed page

// Prevent multiple initializations (in case script is loaded twice)
if (window._homeJsInitialized) {
    console.warn('home.js already initialized, skipping duplicate init');
} else {
    window._homeJsInitialized = true;

(function () {
    'use strict';

    // ================== Dropdown Functionality ==================
    function initDropdowns() {
        // Settings Dropdown
        const settingsButton = document.getElementById('header-settings-button');
        const settingsMenu = document.getElementById('header-settings-menu');

        // Filter Dropdown
        const filterButton = document.getElementById('header-filter-button');
        const filterMenu = document.getElementById('header-filter-menu');

        function toggleDropdown(button, menu, closeOtherMenu) {
            if (!button || !menu) return;

            const isOpen = menu.style.display !== 'none';

            if (isOpen) {
                closeDropdown(menu, button);
            } else {
                // Close other dropdown if provided
                if (closeOtherMenu) {
                    const otherButton = closeOtherMenu === settingsMenu ? settingsButton : filterButton;
                    closeDropdown(closeOtherMenu, otherButton);
                }
                openDropdown(menu, button);
            }
        }

        function openDropdown(menu, button) {
            menu.style.display = 'block';
            button.setAttribute('aria-expanded', 'true');
            // Focus first menu item for keyboard navigation
            const firstItem = menu.querySelector('[role="menuitem"]');
            if (firstItem) {
                setTimeout(() => firstItem.focus(), 50);
            }
        }

        function closeDropdown(menu, button) {
            menu.style.display = 'none';
            if (button) {
                button.setAttribute('aria-expanded', 'false');
                button.focus(); // Return focus to button
            }
        }

        // Settings dropdown handlers
        if (settingsButton && settingsMenu) {
            settingsButton.addEventListener('click', function (e) {
                e.stopPropagation();
                toggleDropdown(settingsButton, settingsMenu, filterMenu);
            });

            // Keyboard support
            settingsButton.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleDropdown(settingsButton, settingsMenu, filterMenu);
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (settingsMenu.style.display === 'none') {
                        openDropdown(settingsMenu, settingsButton);
                    }
                }
            });

            // Keyboard navigation within menu
            settingsMenu.addEventListener('keydown', function (e) {
                const items = Array.from(settingsMenu.querySelectorAll('[role="menuitem"]'));
                const currentIndex = items.indexOf(document.activeElement);

                if (e.key === 'Escape') {
                    closeDropdown(settingsMenu, settingsButton);
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % items.length;
                    items[nextIndex].focus();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                    items[prevIndex].focus();
                } else if (e.key === 'Home') {
                    e.preventDefault();
                    items[0].focus();
                } else if (e.key === 'End') {
                    e.preventDefault();
                    items[items.length - 1].focus();
                }
            });
        }

        // Filter dropdown handlers
        if (filterButton && filterMenu) {
            filterButton.addEventListener('click', function (e) {
                e.stopPropagation();
                toggleDropdown(filterButton, filterMenu, settingsMenu);
            });

            // Keyboard support
            filterButton.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleDropdown(filterButton, filterMenu, settingsMenu);
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (filterMenu.style.display === 'none') {
                        openDropdown(filterMenu, filterButton);
                    }
                }
            });

            // Keyboard navigation within menu
            filterMenu.addEventListener('keydown', function (e) {
                const items = Array.from(filterMenu.querySelectorAll('[role="menuitem"]'));
                const currentIndex = items.indexOf(document.activeElement);

                if (e.key === 'Escape') {
                    closeDropdown(filterMenu, filterButton);
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % items.length;
                    items[nextIndex].focus();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                    items[prevIndex].focus();
                } else if (e.key === 'Home') {
                    e.preventDefault();
                    items[0].focus();
                } else if (e.key === 'End') {
                    e.preventDefault();
                    items[items.length - 1].focus();
                }
            });
        }

        // Close dropdowns when clicking outside (using event delegation for performance)
        let clickOutsideHandler = null;
        function setupClickOutside() {
            if (clickOutsideHandler) return; // Already set up

            clickOutsideHandler = function (e) {
                const target = e.target;

                // Check if this was marked as a vote button click by the isolation handler
                if (e.voteButtonClick) {
                    return; // Don't interfere with vote button clicks
                }

                // Don't interfere with vote buttons, form inputs, textareas, or buttons inside forms
                // Explicitly check for vote buttons first to prevent misrouting clicks
                // Check both the target and its parent elements (for SVG clicks inside buttons)
                const voteSection = target.closest('.vote-section-absolute') || target.closest('.vote-pill');
                const voteButton = target.closest('.vote-button') ||
                    target.closest('.upvote-button') ||
                    target.closest('.downvote-button') ||
                    target.closest('.vote-btn');

                // Also check if target is SVG inside a vote button
                const isVoteButtonSVG = target.tagName === 'svg' && (target.closest('.vote-button') || target.closest('.vote-btn'));
                const isVoteButtonPath = target.tagName === 'path' && (target.closest('.vote-button') || target.closest('.vote-btn'));
                const isVoteButtonPolyline = target.tagName === 'polyline' && (target.closest('.vote-button') || target.closest('.vote-btn'));

                if (voteSection || voteButton ||
                    target.classList.contains('vote-button') ||
                    target.classList.contains('upvote-button') ||
                    target.classList.contains('downvote-button') ||
                    target.classList.contains('vote-btn') ||
                    isVoteButtonSVG || isVoteButtonPath || isVoteButtonPolyline) {
                    // Don't interfere with vote button clicks - return immediately
                    return; // Let vote button clicks proceed normally to their onclick handlers
                }

                // Don't interfere with search form and search button
                const isSearchForm = target.closest('.header-search-form');
                const isSearchButton = target.closest('.header-search-button') || target.classList.contains('header-search-button');
                const isSearchInput = target.classList.contains('header-search-input') || target.id === 'header-search-input';

                if (isSearchForm || isSearchButton || isSearchInput) {
                    return; // Let search form interactions proceed normally
                }

                // Don't interfere with form inputs, textareas, or buttons inside forms
                if (target.tagName === 'INPUT' ||
                    target.tagName === 'TEXTAREA' ||
                    target.tagName === 'BUTTON' ||
                    target.closest('form') ||
                    target.closest('.form-field') ||
                    target.closest('.comment-form') ||
                    target.closest('.post-form')) {
                    return; // Let form interactions proceed normally
                }

                const isSettingsClick = settingsButton && (settingsButton.contains(target) || settingsMenu.contains(target));
                const isFilterClick = filterButton && (filterButton.contains(target) || filterMenu.contains(target));

                if (!isSettingsClick && settingsMenu) {
                    closeDropdown(settingsMenu, settingsButton);
                }
                if (!isFilterClick && filterMenu) {
                    closeDropdown(filterMenu, filterButton);
                }
            };

            // Use capture phase for better performance
            // But ensure vote buttons are completely excluded from click outside handler
            document.addEventListener('click', clickOutsideHandler, true);
        }

        // Close dropdowns on ESC key (global handler)
        // Only handle Escape if dropdowns are open, don't interfere with form inputs
        document.addEventListener('keydown', function (e) {
            // Don't interfere with Escape key in form inputs/textareas unless dropdowns are open
            const target = e.target;
            const isFormInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA';
            const hasOpenDropdown = (settingsMenu && settingsMenu.style.display !== 'none') ||
                (filterMenu && filterMenu.style.display !== 'none');

            if (e.key === 'Escape' && (hasOpenDropdown || !isFormInput)) {
                if (settingsMenu && settingsMenu.style.display !== 'none') {
                    closeDropdown(settingsMenu, settingsButton);
                }
                if (filterMenu && filterMenu.style.display !== 'none') {
                    closeDropdown(filterMenu, filterButton);
                }
            }
        });

        // Initialize click outside handler
        setupClickOutside();
    }

    // ================== Search Functionality ==================
    function initSearchFunctionality() {
        // Try both old and new search input IDs for backward compatibility
        const searchInput = document.getElementById('header-search-input') || document.getElementById('search-input');
        const searchForm = document.querySelector('.header-search-form') || document.querySelector('.search-form');
        const searchWrapper = document.querySelector('.header-search-wrapper') || document.querySelector('.search-wrapper');
        let debounceTimer;
        let suggestionsContainer = null;

        if (searchInput && searchForm && searchWrapper) {
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
            searchInput.addEventListener('blur', function () {
                setTimeout(() => {
                    suggestionsContainer.style.display = 'none';
                }, 200);
            });

            // Show suggestions on focus if there's a query
            searchInput.addEventListener('focus', function () {
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
        const postAsIdentityCheckbox = document.getElementById('id_post_as_identity');

        if (value === 'anonymous') {
            // Anonymous: is_anonymous = True, post_as_identity = False
            if (isAnonymousCheckbox) isAnonymousCheckbox.checked = true;
            if (postAsIdentityCheckbox) postAsIdentityCheckbox.checked = false;
        } else {
            // Profile Identity: is_anonymous = False, post_as_identity = True
            if (isAnonymousCheckbox) isAnonymousCheckbox.checked = false;
            if (postAsIdentityCheckbox) postAsIdentityCheckbox.checked = true;
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
        const WORD_LIMIT = 150; // ~15 lines of text
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
        // FAB is now conditionally rendered in template:
        // - Only shown on Home view (not Create Post view)
        // - Always visible when present (has 'visible' class in HTML)
        // No scroll-based visibility needed anymore
        const fab = document.getElementById('fab-share-thought');
        if (!fab) return;

        // Ensure FAB stays visible (template already adds 'visible' class)
        fab.classList.add('visible');
    }

    // ================== Modal Logic ==================
    function initModalLogic() {
        const postForm = document.getElementById('post-form');
        const staticContainer = document.getElementById('post-form-content');
        const modalContainer = document.getElementById('modal-form-container');
        const modal = document.getElementById('post-modal');

        window.openPostModal = function () {
            if (!postForm || !modalContainer) return;
            modalContainer.appendChild(postForm);
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        };

        window.closePostModal = function () {
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
            }
        }
    }

    // ================== Vote Handling ==================
    window.handleVote = async function (postId, voteType, btnElement) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (!csrfToken) {
            alert('Please log in to vote.');
            return;
        }

        // Normalize voteType for URL
        const urlType = voteType.toLowerCase().replace('vote', '');
        const url = `/posts/${postId}/${urlType}vote/`;

        // Find elements
        const postCard = document.querySelector(`.post-card[data-post-id="${postId}"]`);
        if (!postCard) return;

        const scoreElement = document.getElementById(`vote-score-${postId}`);
        const upBtn = postCard.querySelector('.vote-btn.upvote');
        const downBtn = postCard.querySelector('.vote-btn.downvote');

        // --- Optimistic UI Update ---
        // 1. Determine current state
        const isUpActive = upBtn && upBtn.classList.contains('active');
        const isDownActive = downBtn && downBtn.classList.contains('active');
        let currentScore = parseInt(scoreElement.textContent) || 0;

        // 2. Calculate new state locally
        let newScore = currentScore;
        let newUpState = false;
        let newDownState = false;

        if (voteType === 'UPVOTE') {
            if (isUpActive) {
                // Toggling off upvote
                newScore -= 1;
                newUpState = false;
            } else {
                // Toggling on upvote
                newScore += 1;
                newUpState = true;
                if (isDownActive) {
                    newScore += 1; // Reclaim the downvote point too
                }
            }
        } else if (voteType === 'DOWNVOTE') {
            if (isDownActive) {
                // Toggling off downvote
                newScore += 1;
                newDownState = false;
            } else {
                // Toggling on downvote
                newScore -= 1;
                newDownState = true;
                if (isUpActive) {
                    newScore -= 1; // Reclaim the upvote point too
                }
            }
        }

        // 3. Apply Visuals Immediately
        if (scoreElement) scoreElement.textContent = newScore;
        if (upBtn) upBtn.classList.toggle('active', newUpState);
        if (downBtn) downBtn.classList.toggle('active', newDownState);

        // 4. Send Request
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                // Revert on failure (simple reload or alert, for now just alert)
                if (response.status === 403) {
                    alert('Please log in to vote.');
                    window.location.href = '/auth/login/';
                } else {
                    alert('Vote failed.');
                }
                // Optional: Revert UI here if needed, but for now assuming success or refresh
                return;
            }

            const data = await response.json();

            if (data.success) {
                if (scoreElement && data.upvotes_count !== undefined) {
                    // Calculate score: Up - Down
                    const up = parseInt(data.upvotes_count || 0);
                    const down = parseInt(data.downvotes_count || 0);
                    const score = up - down;
                    console.log('New score:', score);
                    scoreElement.textContent = score;
                }

                // Update Button States
                const buttons = postCard.querySelectorAll('.vote-btn');
                buttons.forEach(btn => btn.classList.remove('active'));

                if (data.user_vote === 'UPVOTE') {
                    const upBtn = postCard.querySelector('.vote-btn.upvote');
                    if (upBtn) upBtn.classList.add('active');
                } else if (data.user_vote === 'DOWNVOTE') {
                    const downBtn = postCard.querySelector('.vote-btn.downvote');
                    if (downBtn) downBtn.classList.add('active');
                }
            } else {
                alert(data.message || 'Vote failed.');
            }
        } catch (e) {
            console.error('Vote error:', e);
            // alert('Network error. Vote may not have saved.');
        } finally {
            // Re-enable if needed, or keep enabled
            // buttons.forEach(b => b.disabled = false); 
        }
    };

    // ================== Search Highlighting ==================
    function initSearchHighlight() {
        // Get 'q' param from URL
        const params = new URLSearchParams(window.location.search);
        const query = params.get('q');

        if (!query || query.trim() === '') return;

        const term = query.trim();
        const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');

        document.querySelectorAll('.post-body-content').forEach(el => {
            // Simple text walker to avoid breaking HTML
            const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
            const nodes = [];
            while (walker.nextNode()) nodes.push(walker.currentNode);

            nodes.forEach(node => {
                if (node.nodeValue && regex.test(node.nodeValue)) {
                    const span = document.createElement('span');
                    span.innerHTML = node.nodeValue.replace(regex, '<span class="highlight">$1</span>');
                    node.parentNode.replaceChild(span, node);
                }
            });
        });
    }

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

    // ================== Post Form Loading State ==================
    function initPostFormLoading() {
        const postForm = document.getElementById('post-form');
        if (!postForm) return;

        const submitBtn = postForm.querySelector('#submit-button');
        if (!submitBtn) return;

        // Create loading overlay
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'post-loading-overlay';
        loadingOverlay.innerHTML = `
            <div class="post-loading-content">
                <div class="loading-spinner"></div>
                <p class="loading-text">Posting...</p>
            </div>
        `;
        loadingOverlay.style.display = 'none';
        postForm.style.position = 'relative';
        postForm.appendChild(loadingOverlay);

        postForm.addEventListener('submit', function(e) {
            // Show loading state
            loadingOverlay.style.display = 'flex';
            submitBtn.disabled = true;
            submitBtn.textContent = 'Posting...';

            // Let form submit normally (don't prevent default)
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
        const btn = document.getElementById(`reply-btn-${postId}`);

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
    // ================== Vote Button Click Isolation ==================
    function initVoteButtonHandlers() {
        // Event delegation for vote buttons
        document.body.addEventListener('click', function (e) {
            // Check if click is on a vote button or its children
            const btn = e.target.closest('.vote-btn');
            if (!btn) return;

            // Allow default behavior? No, we handle it.
            e.preventDefault();
            e.stopPropagation();

            const postId = btn.dataset.postId;
            const voteType = btn.dataset.voteType; // UPVOTE or DOWNVOTE

            if (postId && voteType) {
                window.handleVote(postId, voteType, btn);
            }
        });
    }


    document.addEventListener('DOMContentLoaded', function () {
        initVoteButtonHandlers(); // Initialize delegated vote handler
        initDropdowns();
        initSearchFunctionality();
        initHashtagDetection();
        initIdentityState();
        initPostCollapse();
        initFABVisibility();
        initModalLogic();
        initFlagForms();
        initAutoScroll();
        initSearchHighlight();
        initPostFormLoading(); // Loading indicator for post submission

        // AI Tag Suggestions needs URL from template
        const suggestTagsUrl = document.querySelector('[data-suggest-tags-url]')?.dataset.suggestTagsUrl;
        if (suggestTagsUrl) {
            initAITagSuggestions(suggestTagsUrl);
        }
    });

})();

} // End of initialization guard
