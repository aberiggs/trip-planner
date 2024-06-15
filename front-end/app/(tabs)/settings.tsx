import Ionicons from '@expo/vector-icons/Ionicons';

import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedButton } from '@/components/ThemedButton';
import { ColorTypes } from "@/constants/Colors";

import { Link } from "expo-router";

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
        <ThemedButton style={{flexDirection: "row", alignItems: "center", justifyContent: "space-around", gap: 5}}>
          <Ionicons size={26} name="log-out" />
          <ThemedText color={ColorTypes.background}>Logout</ThemedText>
        </ThemedButton>
      </Link>
    </ThemedView>
  );
}
