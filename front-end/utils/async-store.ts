import AsyncStorage from "@react-native-async-storage/async-storage"

export const saveItem = async (key: string, value: string) => {
  await AsyncStorage.setItem(key, value)
}

export const getItem = async (key: string) => {
  let result = await AsyncStorage.getItem(key)
  return result
}

export const removeItem = async (key: string) => {
  await AsyncStorage.removeItem(key)
}
