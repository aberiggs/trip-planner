import { Link } from "expo-router"

import { ThemedView } from "@/components/ThemedView"
import { ThemedText } from "@/components/ThemedText"
import { ThemedButton } from "@/components/ThemedButton"
import { ThemedIcon } from "@/components/ThemedIcon"

import { ColorTypes } from "@/constants/Colors"

export default function Settings() {
  return (
    <ThemedView
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Link replace href="/" asChild>
        <ThemedButton
          style={{
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "space-around",
            gap: 5,
          }}
        >
          <ThemedIcon color={ColorTypes.base} size={26} name="log-out" />
          <ThemedText color={ColorTypes.base}>Logout</ThemedText>
        </ThemedButton>
      </Link>
    </ThemedView>
  )
}
