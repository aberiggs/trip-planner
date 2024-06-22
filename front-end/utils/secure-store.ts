import * as SecureStore from "expo-secure-store";

export const saveSecret = async (key: string, value: string) => {
  await SecureStore.setItemAsync(key, value);
};

export const getSecret = async (key: string) => {
  let result = await SecureStore.getItemAsync(key);
  return result;
};

export const removeSecret = async (key: string) => {
  await SecureStore.deleteItemAsync(key);
};
