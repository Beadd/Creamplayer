export function openDatabase(database, store) {
  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(database, 1);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      db.createObjectStore(store);
    };

    request.onsuccess = (event) => {
      const db = event.target.result;
      resolve(db);
    };

    request.onerror = (event) => {
      console.error('Failed to open IndexedDB:', event.target.error);
      reject(event.target.error);
    };
  });
}

export function getDatabase(db, key, store) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(store);
    const objectStore = transaction.objectStore(store);
    const request = objectStore.get(key);

    request.onsuccess = (event) => {
      const value = event.target.result;
      resolve(value);
    };

    request.onerror = (event) => {
      console.error('Failed to get data from IndexedDB:', event.target.error);
      reject(event.target.error);
    };
  });
}

export function addDatabase(db, key, value, store) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(store, 'readwrite');
    const objectStore = transaction.objectStore(store);
    const request = objectStore.put(value, key);

    request.onsuccess = () => {
      resolve();
    };

    request.onerror = (event) => {
      console.error('Failed to add data to IndexedDB:', event.target.error);
      reject(event.target.error);
    };
  });
}

export function closeDatabase(db) {
  if (db) {
    db.close();
    db = null;
  }
}

