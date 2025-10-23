/**
 * Format date to readable string
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
export const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Format date and time
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date and time
 */
export const formatDateTime = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Truncate long text with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 50) => {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Capitalize first letter of each word
 * @param {string} text - Text to capitalize
 * @returns {string} Capitalized text
 */
export const capitalizeWords = (text) => {
  if (!text) return '';
  return text
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

/**
 * Get plural form of word based on count
 * @param {number} count - Count of items
 * @param {string} singular - Singular form
 * @param {string} plural - Plural form (optional)
 * @returns {string} Correct form with count
 */
export const pluralize = (count, singular, plural = null) => {
  const pluralForm = plural || `${singular}s`;
  return `${count} ${count === 1 ? singular : pluralForm}`;
};

/**
 * Download file from blob
 * @param {Blob} blob - File blob
 * @param {string} filename - File name
 */
export const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

/**
 * Generate filename with current date
 * @param {string} prefix - Filename prefix
 * @param {string} extension - File extension
 * @returns {string} Filename with date
 */
export const generateFilename = (prefix = 'export', extension = 'xlsx') => {
  const date = new Date();
  const dateStr = date.toLocaleDateString('en-GB').replace(/\//g, '_');
  const timeStr = date.toLocaleTimeString('en-GB', { hour12: false }).replace(/:/g, '_');
  return `${prefix}_${dateStr}_${timeStr}.${extension}`;
};

/**
 * Debounce function - delays execution
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export const debounce = (func, delay = 300) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Check if string is empty or whitespace
 * @param {string} str - String to check
 * @returns {boolean} True if empty
 */
export const isEmpty = (str) => {
  return !str || str.trim().length === 0;
};

/**
 * Sort families by name
 * @param {Array} families - Array of family objects
 * @param {string} order - 'asc' or 'desc'
 * @returns {Array} Sorted families
 */
export const sortFamilies = (families, order = 'asc') => {
  return [...families].sort((a, b) => {
    const nameA = a.family_name.toLowerCase();
    const nameB = b.family_name.toLowerCase();
    
    if (order === 'asc') {
      return nameA.localeCompare(nameB);
    } else {
      return nameB.localeCompare(nameA);
    }
  });
};

/**
 * Get total member count from families array
 * @param {Array} families - Array of family objects
 * @returns {number} Total members
 */
export const getTotalMembers = (families) => {
  return families.reduce((total, family) => {
    return total + (family.member_count || 0);
  }, 0);
};

/**
 * Handle API errors and return user-friendly message
 * @param {Error} error - Error object
 * @returns {string} Error message
 */
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error
    return error.response.data.error || 'Server error occurred';
  } else if (error.request) {
    // No response from server
    return 'Unable to connect to server. Please check if backend is running.';
  } else {
    // Other errors
    return error.message || 'An unexpected error occurred';
  }
};
