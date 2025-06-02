import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useFonts } from 'expo-font';
import { View, ActivityIndicator } from 'react-native';

import HomeScreen from './screens/HomeScreen';
import IdeasScreen from './screens/IdeasScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();

export type RootStackParamList = {
  Home: undefined;
  Ideas: { formData: Record<string, string> };
};

export default function App() {
  const [fontsLoaded] = useFonts({
    Inter: require('./assets/fonts/Inter_18pt-Regular.ttf'),
    'Inter-Medium': require('./assets/fonts/Inter_18pt-Medium.ttf'),
    'Inter-SemiBold': require('./assets/fonts/Inter_18pt-SemiBold.ttf'),
    'Inter-Bold': require('./assets/fonts/Inter_18pt-Bold.ttf'),
  });



  if (!fontsLoaded) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Ideas"
          component={IdeasScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>      
    </NavigationContainer>
  );
}