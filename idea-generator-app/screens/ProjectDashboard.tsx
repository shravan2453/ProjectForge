// ProjectDashboard.tsx (Converted to NativeWind)
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, FlatList, Dimensions } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';

const COLOR_PALETTE = [
  '#FFE29A', // light yellow
  '#B5F7D0', // light mint
  '#AEEBFF', // light blue
  '#FFD6E0', // light pink
  '#FFF3B0', // pale gold
  '#D1F2EB', // light teal
  '#E0BBE4', // light lavender
  '#FFECB3', // light cream
  '#F8B195', // light coral
  '#F6DFEB', // light blush
];

const CARD_WIDTH = Math.min(Dimensions.get('window').width * 0.9, 400);

export default function ProjectDashboard() {
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const route = useRoute();
  // Store projects as an array of ideas
  const [projects, setProjects] = useState<any[]>(() => {
    const initial = (route.params as any)?.selectedIdea;
    return initial ? [initial] : [];
  });
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  // Add new project if navigated with selectedIdea
  React.useEffect(() => {
    const newIdea = (route.params as any)?.selectedIdea;
    if (newIdea && !projects.some((p) => p.name === newIdea.name)) {
      setProjects((prev) => [newIdea, ...prev]);
    }
    // eslint-disable-next-line
  }, [(route.params as any)?.selectedIdea]);

  // Pick a random color for each project (stable per project)
  const getColor = (name: string) => {
    let hash = 0;
    for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
    return COLOR_PALETTE[Math.abs(hash) % COLOR_PALETTE.length];
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: 'white' }}>
      <View style={{ width: '100%', maxWidth: 420, alignItems: 'center' }}>
        <Text className="text-3xl text-black mb-6" style={{ fontFamily: 'Klados-Bold', textAlign: 'center' }}>Your Projects</Text>

        <FlatList
          data={projects}
          keyExtractor={(item) => item.name}
          style={{ width: '100%' }}
          contentContainerStyle={{ alignItems: 'center', paddingBottom: 16, minHeight: 80 }}
          ListEmptyComponent={
            <Text className="text-base text-gray-500 mb-8 text-center" style={{ fontFamily: 'Klados-Bold' }}>
              No projects yet. Create your first one!
            </Text>
          }
          renderItem={({ item, index }) => {
            const expanded = expandedIndex === index;
            return (
              <TouchableOpacity
                activeOpacity={0.9}
                onPress={() => setExpandedIndex(expanded ? null : index)}
                style={{
                  backgroundColor: getColor(item.name),
                  borderRadius: 12,
                  padding: 16,
                  marginBottom: 14,
                  width: CARD_WIDTH,
                  shadowColor: '#000',
                  shadowOpacity: 0.08,
                  shadowRadius: 8,
                  shadowOffset: { width: 0, height: 2 },
                  minHeight: 48,
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Text style={{ fontFamily: 'Klados-Bold', fontSize: 16, color: '#222', textAlign: 'center' }}>{item.name}</Text>
                {expanded && (
                  <View style={{ marginTop: 8, width: '100%' }}>
                    {item.skills && (
                      <>
                        <Text style={{ fontFamily: 'Klados-Bold', color: '#444', fontSize: 13, marginBottom: 2 }}>Skills:</Text>
                        <Text style={{ color: '#222', fontSize: 14, marginBottom: 6 }}>{item.skills}</Text>
                      </>
                    )}
                    <Text style={{ fontFamily: 'Klados-Bold', color: '#444', fontSize: 13, marginBottom: 2 }}>Overview:</Text>
                    <Text style={{ color: '#222', fontSize: 14, marginBottom: 6 }}>{item.overview}</Text>
                    <Text style={{ fontFamily: 'Klados-Bold', color: '#444', fontSize: 13, marginBottom: 2 }}>Difficulty:</Text>
                    <Text style={{ color: '#222', fontSize: 14, marginBottom: 6 }}>{item.difficulty}</Text>
                    <Text style={{ fontFamily: 'Klados-Bold', color: '#444', fontSize: 13, marginBottom: 2 }}>Timeline:</Text>
                    <Text style={{ color: '#222', fontSize: 14 }}>{item.timeline}</Text>
                  </View>
                )}
              </TouchableOpacity>
            );
          }}
        />

        <TouchableOpacity
          style={{ backgroundColor: 'black', paddingVertical: 16, paddingHorizontal: 32, borderRadius: 14, marginBottom: 32, width: CARD_WIDTH, alignItems: 'center' }}
          onPress={() => navigation.navigate('Form')}
        >
          <Text className="text-white text-base font-semibold" style={{ fontFamily: 'Klados-Bold', textAlign: 'center' }}>+ Create New Project</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={{ marginBottom: 24 }}
          onPress={() => navigation.replace('HomeLogin')}
        >
          <Text className="text-gray-600 text-sm underline" style={{ fontFamily: 'Klados-Bold', textAlign: 'center' }}>Log Out</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
