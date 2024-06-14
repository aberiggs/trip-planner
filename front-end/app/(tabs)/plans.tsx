import { Text, View } from "react-native";
import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ScrollView } from "react-native";

export default function Plans() {
  return (
    <ScrollView style={{flex: 1}}>
      <ThemedView
        style={{
          flex: 1,
          height: "100%",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <ThemedText>These are your plans.</ThemedText>
      </ThemedView>
    </ScrollView>
  );
}

