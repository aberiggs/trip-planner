import { View, Text, Button } from "react-native";
import { StyleSheet } from "react-native";
import * as WebBrowser from "expo-web-browser";
import * as Google from "expo-auth-session/providers/google"
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";

WebBrowser.maybeCompleteAuthSession();

const styles = StyleSheet.create({
  centered: { 
    flex: 1, 
    justifyContent: "center", 
    alignItems: "center", 
  }, 
  title: { 
    fontSize: 18, 
    marginVertical: 2, 
  }, 
  subtitle: { 
    fontSize: 14, 
  }
});

interface User {
  "email": string
  "picture": string
  "name": string
}

interface JwtHeader {
  alg: string,
  exp: number, 
  typ: string
}

export default function Index() {
  const [userInfo, setUserInfo] = useState<User | null>(null);

  const [request, fullResult, promptAsync] = Google.useIdTokenAuthRequest({
    iosClientId: process.env.EXPO_PUBLIC_IOS_CLIENT_ID,
    webClientId: process.env.EXPO_PUBLIC_WEB_CLIENT_ID,
    scopes: ["profile", "email"],
  });

  useEffect(() => {
    handleGoogleSignIn();
  }, [fullResult])

  const handleGoogleSignIn = async() => {
    const user = await AsyncStorage.getItem("user");
    const jwtToken = await AsyncStorage.getItem("jwt");

    if (!user || !jwtToken) {
      if (fullResult?.type === "success") {
        const response = await fetch("http://127.0.0.1:3000/auth", {
          method: "POST",
          body: JSON.stringify({
            "idToken": fullResult.params.id_token
          }),
          headers: {
            "Content-Type": "application/json"
          }
        })
        const data = await response.json();
        const jwtToken = data["jwt"]
        const user = jwtDecode<User>(jwtToken);
        const header = jwtDecode<JwtHeader>(jwtToken, { header: true });

        // TODO: check jwt token has not expired
        await AsyncStorage.setItem("user", JSON.stringify(user));
        await AsyncStorage.setItem("jwt", jwtToken);
        setUserInfo(user);
      }
    }
    else {
      setUserInfo(JSON.parse(user))
    }
  }

  return (
    <View style={styles.centered}>
      <Text>{JSON.stringify(userInfo, null, 2)}</Text>
      <Text>Login</Text>
      <Button title="sign in with google" onPress={() => promptAsync()} />
      <Button title="delete local storage" onPress={() => AsyncStorage.removeItem("user")}></Button>
    </View>
  );
}
