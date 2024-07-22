import { Link } from "expo-router"

import { ThemedView } from "@/components/ThemedView"
import { ThemedText } from "@/components/ThemedText"
import { HelloWave } from "@/components/HelloWave"
import { getSecret, removeSecret } from "@/utils/secure-store"
import { removeItem } from "@/utils/async-store"
import { Button } from "react-native"

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
  console.log(data)
}

export default function Landing() {
  return (
    <ThemedView
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <ThemedView
        style={{
          flex: 0.4,
          flexDirection: "column",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <ThemedText style={{ fontSize: 40 }}>
          Welcome <HelloWave />
        </ThemedText>
        <Link href="/login">Login Page</Link>
        <Link href={"(tabs)/plans"}>go to tabs</Link>
        <Button title="test login" onPress={() => testLogin()} />
        <Button
          title="delete local storage"
          onPress={() => {
            removeItem("user")
            removeSecret("jwt")
          }}
        />
      </ThemedView>
    </ThemedView>
  )
}
