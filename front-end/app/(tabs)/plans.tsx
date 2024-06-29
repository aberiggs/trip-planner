import React from "react";

import { ThemedView } from "@/components/ThemedView";
import { ThemedText } from '@/components/ThemedText';
import { ThemedFlatList } from "@/components/ThemedFlatList";

import { ColorTypes } from "@/constants/Colors";

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
      color={ColorTypes.primary}
    >
      <ThemedText color={ColorTypes.base}>{plan.name}</ThemedText>
      <ThemedText color={ColorTypes.base}>{plan.date.toDateString()}</ThemedText>
    </ThemedView>
  );
}

type Plan = {
  name: string;
  date: Date;
};

// Create a Plan data array for testing
const PlansData: Plan[] = [
  { name: "Day Trip", date: new Date(Date.parse("2024-08-3")) },
  { name: "Bellevue Trip", date: new Date(Date.parse("2024-06-20")) },
  { name: "<Generic Name>", date: new Date(Date.parse("2024-07-10")) },
];

