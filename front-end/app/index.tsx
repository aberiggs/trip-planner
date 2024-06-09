import { Pressable, Text, View } from "react-native";
import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedButton } from '@/components/ThemedButton';

export default function Landing() {
  return (
    <ThemedView 
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <ThemedText>Welcome!</ThemedText>

      <ThemedButton onPress={() => navigation.navigate('plans')}>Go To Home</ThemedButton>
    </ThemedView>
  );
}
