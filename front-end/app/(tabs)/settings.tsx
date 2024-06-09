import { Text, View } from "react-native";
import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';

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
    </ThemedView>
  );
}

