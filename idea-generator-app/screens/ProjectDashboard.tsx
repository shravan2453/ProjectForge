// ProjectDashboard.tsx (Converted to NativeWind)
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, FlatList } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function ProjectDashboard() {
  const navigation = useNavigation<NavigationProp>();
  const [projects, setProjects] = useState<any[]>([]); // Future: replace 'any' with a proper type

  return (
    <View className="flex-1 bg-white px-6 justify-center items-center">
      <Text className="text-3xl text-black mb-4" style={{ fontFamily: 'Klados-Bold' }}>Your Projects</Text>

      {projects.length === 0 ? (
        <Text className="text-base text-gray-500 mb-8 text-center" style={{ fontFamily: 'Klados-Bold' }}>
          No projects yet. Create your first one!
        </Text>
      ) : (
        <FlatList
          data={projects}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View className="w-full border border-gray-300 rounded-lg p-4 mb-3"> 
              <Text className="text-black text-base">{item.name}</Text>
            </View>
          )}
        />
      )}

      <TouchableOpacity
        className="bg-black py-4 px-10 rounded-xl mt-6"
        onPress={() => navigation.navigate('Form')}
      >
        <Text className="text-white text-base font-semibold" style={{ fontFamily: 'Klados-Bold' }}>+ Create New Project</Text>
      </TouchableOpacity>

      <TouchableOpacity
        className="mt-5"
        onPress={() => navigation.navigate('HomeLogin')}
      >
        <Text className="text-gray-600 text-sm underline" style={{ fontFamily: 'Klados-Bold' }}>Log Out</Text>
      </TouchableOpacity>
    </View>
  );
}
