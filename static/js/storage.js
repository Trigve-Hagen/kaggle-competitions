/**
 * A class to manage interactions with localStorage, handling JSON serialization.
 */
class StorageManager {
  /**
   * Saves data to localStorage under a specific key.
   * Automatically stringifies objects/arrays.
   * @param {string} key The key under which to store the data.
   * @param {any} value The data to store (will be stringified if not a string).
   */
  static setItem(key, value) {
    try {
      const serializedValue = typeof value === 'string' ? value : JSON.stringify(value);
      localStorage.setItem(key, serializedValue);
      console.log(`Saved item with key: ${key}`);
    } catch (error) {
      console.error(`Error saving item to localStorage for key "${key}":`, error);
    }
  }

  /**
   * Retrieves data from localStorage for a specific key.
   * Automatically parses JSON strings.
   * Returns null if the item doesn't exist or an error occurs during parsing.
   * @param {string} key The key of the item to retrieve.
   * @returns {any|null} The retrieved data (parsed if JSON), or null.
   */
  static getItem(key) {
    try {
      const storedValue = localStorage.getItem(key);
      if (storedValue === null) {
        return null;
      }
      // Try to parse the value as JSON; if it fails, return the raw string
      try {
        return JSON.parse(storedValue);
      } catch (error) {
        return storedValue;
      }
    } catch (error) {
      console.error(`Error retrieving item from localStorage for key "${key}":`, error);
      return null;
    }
  }

  /**
   * Removes a specific item from localStorage.
   * @param {string} key The key of the item to remove.
   */
  static removeItem(key) {
    try {
      localStorage.removeItem(key);
      console.log(`Removed item with key: ${key}`);
    } catch (error) {
      console.error(`Error removing item from localStorage for key "${key}":`, error);
    }
  }

  /**
   * Clears all data from the entire localStorage for the current domain.
   */
  static clearAll() {
    try {
      localStorage.clear();
      console.log('Cleared all localStorage data.');
    } catch (error) {
      console.error('Error clearing all localStorage data:', error);
    }
  }

  /**
   * Checks if localStorage is supported by the browser.
   * @returns {boolean} True if supported, false otherwise.
   */
  static isSupported() {
    try {
      const testKey = '__storage_test__';
      localStorage.setItem(testKey, testKey);
      localStorage.removeItem(testKey);
      return true;
    } catch (e) {
      return false;
    }
  }
}

/*
Saving data:

const userPrefs = { theme: 'dark', notifications: true };
StorageManager.setItem('userPreferences', userPrefs); // Object is automatically stringified
StorageManager.setItem('lastVisit', new Date().toISOString()); // A string can also be saved

Retrieving data:

const preferences = StorageManager.getItem('userPreferences');
console.log(preferences.theme); // 'dark'

const lastVisit = StorageManager.getItem('lastVisit');
console.log(lastVisit); // A string like '2026-02-23T15:29:00.000Z'

Removing data:

StorageManager.removeItem('lastVisit');

Checking support:

if (StorageManager.isSupported()) {
  // Proceed with local storage operations
} else {
  // Use a fallback mechanism (e.g., cookies or server-side storage)
}
*/
