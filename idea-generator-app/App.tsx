import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useFonts } from 'expo-font';
import { View, ActivityIndicator } from 'react-native';

import HomeLogin from './screens/HomeLogin';
//import Signup from './screens/Signup';
import FormScreen from './screens/FormScreen';
import IdeasScreen from './screens/IdeasScreen';
import ProjectDashboard from './screens/ProjectDashboard';
import SignUpScreen from './screens/SignUpScreen';
import ChatScreen from './screens/ChatScreen'; 

export type ParsedIdea = {
  name: string;
  overview: string;
  difficulty: string;
  timeline: string;
};

export type FormDataType = {
  project_type: string;
  project_interest: string;
  project_technical: string;
  project_potential: string;
  project_additional: string;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export type RootStackParamList = {
  HomeLogin: undefined;
  SignUp: undefined;
  Dashboard: undefined;
  Form: undefined;
  Ideas: { formData: FormDataType; retainedIdeas?: ParsedIdea[] };
  Chat: {
    previousMessages: { role: string; content: string }[];
    preferences: string[];
  };
};

export default function App() {
  const [fontsLoaded] = useFonts({
    Inter: require('./assets/fonts/Inter_18pt-Regular.ttf'),
    'Inter-Medium': require('./assets/fonts/Inter_18pt-Medium.ttf'),
    'Inter-SemiBold': require('./assets/fonts/Inter_18pt-SemiBold.ttf'),
    'Inter-Bold': require('./assets/fonts/Inter_18pt-Bold.ttf'),
    'Klados-Main': require('./assets/fonts/Poppins-Light.ttf'),
    'Klados-Bold': require('./assets/fonts/Poppins-SemiBold.ttf'),
    'Klados-Italic': require('./assets/fonts/Poppins-Italic.ttf'),
    'Klados-Ultra-Bold': require('./assets/fonts/Poppins-Bold.ttf'),
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
      <Stack.Navigator initialRouteName="HomeLogin">
        <Stack.Screen
          name="HomeLogin"
          component={HomeLogin}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="SignUp"
          component={SignUpScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Dashboard"
          component={ProjectDashboard}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Form"
          component={FormScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Ideas"
          component={IdeasScreen}
          options={{
            headerShown: false,
            animation: 'slide_from_left'
          }}
        />
        <Stack.Screen
          name="Chat"
          component={ChatScreen}
          options={{
            headerShown: false,
          }}
        />
      </Stack.Navigator>      
    </NavigationContainer>
  );
}
