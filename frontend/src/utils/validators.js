/**
 * Validate family name
 * @param {string} name - Family name
 * @returns {string|null} Error message or null
 */
export const validateFamilyName = (name) => {
  if (!name || name.trim().length === 0) {
    return 'Family name is required';
  }
  if (name.trim().length < 2) {
    return 'Family name must be at least 2 characters';
  }
  if (name.trim().length > 200) {
    return 'Family name is too long (maximum 200 characters)';
  }
  return null;
};

/**
 * Validate address
 * @param {string} address - Address
 * @returns {string|null} Error message or null
 */
export const validateAddress = (address) => {
  if (!address || address.trim().length === 0) {
    return 'Address is required';
  }
  if (address.trim().length < 10) {
    return 'Please enter a complete address';
  }
  if (address.trim().length > 500) {
    return 'Address is too long (maximum 500 characters)';
  }
  return null;
};

/**
 * Validate person name
 * @param {string} name - Person name
 * @returns {string|null} Error message or null
 */
export const validatePersonName = (name) => {
  if (!name || name.trim().length === 0) {
    return 'Name is required';
  }
  if (name.trim().length < 2) {
    return 'Name must be at least 2 characters';
  }
  if (name.trim().length > 200) {
    return 'Name is too long (maximum 200 characters)';
  }
  return null;
};

/**
 * Validate entire family form
 * @param {object} data - Form data
 * @returns {object} Errors object
 */
export const validateFamilyForm = (data) => {
  const errors = {};
  
  const nameError = validateFamilyName(data.family_name);
  if (nameError) errors.family_name = nameError;
  
  const addressError = validateAddress(data.address);
  if (addressError) errors.address = addressError;
  
  return errors;
};

/**
 * Validate person form
 * @param {object} data - Form data
 * @returns {object} Errors object
 */
export const validatePersonForm = (data) => {
  const errors = {};
  
  const nameError = validatePersonName(data.name);
  if (nameError) errors.name = nameError;
  
  return errors;
};
