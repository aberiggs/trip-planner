import { Text, View } from "react-native";
import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedButton } from '@/components/ThemedButton';
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
      <ThemedText>These are your settings.</ThemedText>
      <Link href="/">
        <ThemedButton><Text>Logout</Text></ThemedButton>
      </Link>
    </ThemedView>
  );
}

