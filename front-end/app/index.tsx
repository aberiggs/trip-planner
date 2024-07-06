import { Link } from "expo-router";

import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedButton } from '@/components/ThemedButton';
import { ThemedIcon } from '@/components/ThemedIcon';
import { HelloWave } from "@/components/HelloWave";

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
        <Link replace href="/google-login" asChild>
          <ThemedButton style={{flexDirection: "row", alignItems: "center", justifyContent: "space-around", gap: 10}}>
            <ThemedIcon color={ColorTypes.base} name="logo-google"/>
            <ThemedText color={ColorTypes.base}>Log in with Google</ThemedText>
          </ThemedButton>
        </Link>

      </ThemedView>
    </ThemedView>
  );
}
