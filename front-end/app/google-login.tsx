import { View, Text, Button } from "react-native"
import { StyleSheet } from "react-native"
import * as WebBrowser from "expo-web-browser"
import * as Google from "expo-auth-session/providers/google"
import { useEffect, useState } from "react"
import { jwtDecode } from "jwt-decode"
import { saveItem, getItem, removeItem } from "@/utils/async-store"
import { getSecret, saveSecret, removeSecret } from "@/utils/secure-store"
import { Link } from "expo-router"

WebBrowser.maybeCompleteAuthSession()

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
  },
})

interface User {
  email: string
  picture: string
  name: string
}

interface JwtHeader {
  alg: string
  exp: number
  typ: string
}

export default function Index() {
  const [userInfo, setUserInfo] = useState<User | null>(null)

  /* eslint-disable @typescript-eslint/no-unused-vars */
  const [request, fullResult, promptAsync] = Google.useIdTokenAuthRequest({
    iosClientId: process.env.EXPO_PUBLIC_IOS_CLIENT_ID,
    webClientId: process.env.EXPO_PUBLIC_WEB_CLIENT_ID,
    scopes: ["profile", "email"],
  })

  useEffect(() => {
    handleGoogleSignIn()
  }, [fullResult])

  const handleGoogleSignIn = async () => {
    const user = await getItem("user")
    const jwtToken = await getSecret("jwt")

    if (!user || !jwtToken) {
      if (fullResult?.type === "success") {
        const response = await fetch(
          `${process.env.EXPO_PUBLIC_BACKEND_URL}/auth`,
          {
            method: "POST",
            body: JSON.stringify({
              id_token: fullResult.params.id_token,
              client_type: "ios",
            }),
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        const data = await response.json()
        const jwtToken = data["jwt"]
        const user = jwtDecode<User>(jwtToken)
        const header = jwtDecode<JwtHeader>(jwtToken, { header: true })

        if (Number(header["exp"]) < new Date().getTime()) {
          // jwt token has expired, prompt user to log in again
        }
        await saveItem("user", JSON.stringify(user))
        await saveSecret("jwt", jwtToken)
        setUserInfo(user)
      }
    } else {
      setUserInfo(JSON.parse(user))
    }
  }

  const deleteLocalStorage = () => {
    removeItem("user")
    removeSecret("jwt")
  }

  const testLogin = async () => {
    const jwtToken = await getSecret("jwt")
    const response = await fetch(
      `${process.env.EXPO_PUBLIC_BACKEND_URL}/test_auth`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwtToken}`,
        },
      }
    )
    const data = await response.json()
  }

  return (
    <View style={styles.centered}>
      <Text>{JSON.stringify(userInfo, null, 2)}</Text>
      <Text>Login</Text>
      <Button title="sign in with google" onPress={() => promptAsync()} />
      <Button
        title="delete local storage"
        onPress={() => deleteLocalStorage()}
      />
      <Button title="test login" onPress={() => testLogin()} />
      <Link href="/index">go back</Link>
    </View>
  )
}
