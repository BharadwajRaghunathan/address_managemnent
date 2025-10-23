// API Endpoints (if you want centralized endpoint management)
export const API_ENDPOINTS = {
  FAMILIES: '/families',
  PERSONS: '/persons',
  STATS: '/stats',
  EXPORT_EXCEL: '/export/excel',
  EXPORT_CSV: '/export/csv',
  SEARCH: '/search',
};

// App Configuration
export const APP_CONFIG = {
  NAME: 'Wedding Guest Management',
  VERSION: '1.0.0',
  MAX_FAMILY_NAME_LENGTH: 200,
  MAX_ADDRESS_LENGTH: 500,
  MAX_PERSON_NAME_LENGTH: 200,
};

// Toast/Alert Messages
export const MESSAGES = {
  FAMILY_ADDED: 'Family added successfully!',
  FAMILY_UPDATED: 'Family updated successfully!',
  FAMILY_DELETED: 'Family deleted successfully!',
  MEMBER_ADDED: 'Member added successfully!',
  MEMBER_UPDATED: 'Member updated successfully!',
  MEMBER_DELETED: 'Member removed successfully!',
  EXPORT_SUCCESS: 'Export completed successfully!',
  ERROR_GENERAL: 'Something went wrong. Please try again.',
  ERROR_NETWORK: 'Network error. Please check your connection.',
};

// Validation Rules
export const VALIDATION = {
  FAMILY_NAME_MIN_LENGTH: 2,
  FAMILY_NAME_MAX_LENGTH: 200,
  ADDRESS_MIN_LENGTH: 10,
  ADDRESS_MAX_LENGTH: 500,
  PERSON_NAME_MIN_LENGTH: 2,
  PERSON_NAME_MAX_LENGTH: 200,
};
