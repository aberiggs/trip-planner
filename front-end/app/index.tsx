import { Link } from "expo-router"

import { ThemedView } from "@/components/ThemedView"
import { ThemedText } from "@/components/ThemedText"
import { HelloWave } from "@/components/HelloWave"

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
        <Link href={"/create_activity"}>go to create activity</Link>
      </ThemedView>
    </ThemedView>
  )
}
