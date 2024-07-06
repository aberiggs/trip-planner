import React from 'react';
import { Tabs } from 'expo-router';

import { Pressable } from 'react-native';
import { TabBarIcon } from '@/components/navigation/TabBarIcon';
import { ThemedView } from '@/components/ThemedView';
import { ThemedIcon } from '@/components/ThemedIcon';

import { useColorScheme } from '@/hooks/useColorScheme';
import { ColorTypes, Colors } from '@/constants/Colors';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  const tabsBase = Colors[colorScheme ?? 'light'].base;
  const tabsPrimary = Colors[colorScheme ?? 'light'].primary;

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: tabsPrimary,
        headerTitleStyle: {color: tabsPrimary, fontSize: 22},
        tabBarStyle: {backgroundColor: tabsBase, borderTopWidth: 0},
        headerStyle: {backgroundColor: tabsBase, borderTopWidth: 0},
        headerShadowVisible: false,
        headerShown: true,
      }}>
      <Tabs.Screen
        name="plans"
        options={{
          title: 'Plans',
          headerRight: () => <CreatePlanButton />,
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'create' : 'create-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'settings' : 'settings-outline'} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}

// TODO: Move this out to its own file?
const CreatePlanButton = () => {
  return (
    <ThemedView style={{paddingHorizontal: 25}}>
      <Pressable>
        {({pressed}) => <ThemedIcon name="add" color={ColorTypes.primary} style={[pressed ? {opacity: .5} : {}]} size={26} /> }
      </Pressable>
    </ThemedView>
  )
}
