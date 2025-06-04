// IdeasScreen.tsx (Converted to NativeWind)
import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  TouchableOpacity,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import CustomHeader from '../screens/CustomHeader';

type Props = NativeStackScreenProps<RootStackParamList, 'Ideas'>;
type ParsedIdea = {
  name: string;
  overview: string;
  difficulty: string;
  timeline: string;
};

function clean(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/^\*+\s*/, '')
    .replace(/\*+$/, '')
    .trim();
}

function parseIdeaBlocks(ideas: string[]): ParsedIdea[] {
  const structured: ParsedIdea[] = [];
  let current: Partial<ParsedIdea> = {};

  ideas.forEach((line) => {
    const cleanLine = clean(line);

    if (cleanLine.startsWith('Project Name:')) {
      if (current.name) structured.push(current as ParsedIdea);
      current = { name: cleanLine.replace('Project Name:', '').trim() };
    } else if (cleanLine.startsWith('Project Overview:')) {
      current.overview = cleanLine.replace('Project Overview:', '').trim();
    } else if (cleanLine.startsWith('Project Difficulty:')) {
      current.difficulty = cleanLine.replace('Project Difficulty:', '').trim();
    } else if (cleanLine.startsWith('Project Timeline:')) {
      current.timeline = cleanLine.replace('Project Timeline:', '').trim();
    }
  });

  if (current.name) structured.push(current as ParsedIdea);

  return structured.map((item) => ({
    name: clean(item.name || ''),
    overview: clean(item.overview || ''),
    difficulty: clean(item.difficulty || ''),
    timeline: clean(item.timeline || ''),
  }));
}

export default function IdeasScreen({ route, navigation }: Props) {
  const { formData } = route.params;
  const [ideas, setIdeas] = useState<ParsedIdea[] | null>(null);

  useEffect(() => {
    async function fetchIdeas() {
      try {
        const response = await fetch('http://127.0.0.1:8000/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        const rawIdeas = Array.isArray(data.ideas) ? data.ideas : Object.values(data)[0];
        const parsed = parseIdeaBlocks(rawIdeas);
        setIdeas(parsed);
      } catch (err) {
        console.error('❌ Fetch failed:', err);
      }
    }

    fetchIdeas();
  }, []);

  if (!ideas) {
    return (
      <View className="flex-1 items-center justify-center pt-24 bg-white">
        <ActivityIndicator size="large" />
        <Text className="mt-5 text-gray-500">Generating your ideas...</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={{ paddingBottom: 60 }} className="bg-white px-5">
      <CustomHeader title="Your Project Ideas" showBack />

      {ideas.map((idea, index) => (
        <View key={index} className="bg-gray-100 border border-gray-300 rounded-xl p-4 mb-4">
          <Text className="text-lg font-semibold text-black mb-1">{idea.name}</Text>

          <Text className="text-sm text-gray-600 mt-2">Overview:</Text>
          <Text className="text-base text-gray-800 leading-6">{idea.overview}</Text>

          <Text className="text-sm text-gray-600 mt-2">Difficulty:</Text>
          <Text className="text-base text-gray-800 leading-6">{idea.difficulty}</Text>

          <Text className="text-sm text-gray-600 mt-2">Timeline:</Text>
          <Text className="text-base text-gray-800 leading-6">{idea.timeline}</Text>
        </View>
      ))}

      <TouchableOpacity
        className="mt-5 bg-black py-4 rounded-xl items-center"
        onPress={() => navigation.goBack()}
      >
        <Text className="text-white text-base font-bold">← Back to Form</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}
