import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedButton } from '@/components/ThemedButton';
import { HelloWave } from "@/components/HelloWave";

import { Link } from "expo-router";

import Ionicons from '@expo/vector-icons/Ionicons';
import { ColorTypes } from "@/constants/Colors";

export default function Landing() {
  return (
    <ThemedView 
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <ThemedView style={{
        flex: .4,
        flexDirection: "column",
        justifyContent: "space-between",
        alignItems: "center",
      }}>

        <ThemedText style={{fontSize: 40}}>Welcome <HelloWave/></ThemedText>
        <Link replace href="/plans" asChild>
          <ThemedButton style={{flexDirection: "row", alignItems: "center", justifyContent: "space-around", gap: 10}}>
            <Ionicons size={28} name="logo-google"/>
            <ThemedText color={ColorTypes.background}>Log in with Google</ThemedText>
          </ThemedButton>
        </Link>

      </ThemedView>
    </ThemedView>
  );
}
