import { 
  openDatabase,
  getDatabase,
  addDatabase,
  closeDatabase 
} from './index.js';

export async function initTheme(database, store, settingKey, themeNum) {
  const db = await openDatabase(database, store);
  const value = await getDatabase(db, settingKey, store);
  if (value) {
    themeNum.value = value
    closeDatabase(db)
  } else {
    await addDatabase(db, settingKey, themeNum.value, store);
    closeDatabase(db)
  }
} 

export async function updateTheme(database, store, settingKey, themeNum, newValue) {
  themeNum.value = newValue
  const db = await openDatabase(database, store);
  await addDatabase(db, settingKey, newValue, store);
  closeDatabase(db)
}

export async function setCookie(value) {
  const database = 'CreamPlayer'
  const store = 'Setting'
  const settingKey = 'cookie'
  const db = await openDatabase(database, store);
  await addDatabase(db, settingKey, value, store);
  closeDatabase(db)
}

export async function getCookie() {
  const database = 'CreamPlayer'
  const store = 'Setting'
  const settingKey = 'cookie'

  const db = await openDatabase(database, store);
  const cookie = await getDatabase(db, settingKey, store);
  closeDatabase(db);
  return cookie;
}