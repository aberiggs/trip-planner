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
      <Link replace href="/" asChild>
        <ThemedButton><ThemedText type={"button"}>Logout</ThemedText></ThemedButton>
      </Link>
    </ThemedView>
  );
}
