import { Text } from "react-native";
import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedButton } from '@/components/ThemedButton';

import { Link } from "expo-router";

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
      <Link replace href="/plans">
        <ThemedButton><Text>Go To Home</Text></ThemedButton>
      </Link>
      
    </ThemedView>
  );
}
