import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedFlatList } from "@/components/ThemedFlatList";
import { ColorTypes } from "@/constants/Colors";
import React from "react";

export default function Plans() {
  return (
    <ThemedFlatList 
      contentContainerStyle={{
        flex: 1,
        flexDirection: "column",
        alignItems: "center",
        gap: 20,
        padding: 20,
      }}

      data={PlansData}
      keyExtractor={(item, index) => index.toString()}
      renderItem={({ item }) => <PlanCard plan={item} />}
    >
    </ThemedFlatList>
  );
}

interface PlanCardProps {
  plan: Plan;
}

const PlanCard: React.FC<PlanCardProps> = ({plan}) => {
  return (
    <ThemedView 
      style={{
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        padding: 10,
        width: "100%",
        height: 100,
        borderRadius: 10,
        marginBottom: 10,
      }}
      color={ColorTypes.text}
    >
      <ThemedText color={ColorTypes.background}>{plan.name}</ThemedText>
      <ThemedText color={ColorTypes.background}>{plan.price}</ThemedText>
    </ThemedView>
  );
}

type Plan = {
  name: string;
  price: number;
};

// Create a Plan data array for testing

const PlansData: Plan[] = [
  { name: "Basic", price: 0 },
  { name: "Standard", price: 10 },
  { name: "Premium", price: 20 },
];

