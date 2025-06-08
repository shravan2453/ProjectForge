// IdeasScreen.tsx
import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  TouchableOpacity,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList, ParsedIdea } from '../App';
import CustomHeader from '../screens/CustomHeader';

type Props = NativeStackScreenProps<RootStackParamList, 'Ideas'>;

function clean(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/^\*+\s*/, '')
    .replace(/\*+$/, '')
    .trim();
}

function parseIdeaBlocks(lines: string[]): ParsedIdea[] {
  const structured: ParsedIdea[] = [];
  let current: Partial<ParsedIdea> = {};

  lines.forEach((rawLine) => {
    const line = rawLine.trim();
    if (line.startsWith('Project Name:')) {
      if (current.name) structured.push(current as ParsedIdea);
      current = { name: clean(line.replace('Project Name:', '')).trim() };
    } else if (line.startsWith('Project Overview:')) {
      current.overview = line.replace('Project Overview:', '').trim();
    } else if (line.startsWith('Project Difficulty:')) {
      current.difficulty = line.replace('Project Difficulty:', '').trim();
    } else if (line.startsWith('Project Timeline:')) {
      current.timeline = line.replace('Project Timeline:', '').trim();
    } else if (line !== '') {
      // Append to the last non-empty field for multiline support
      if (current.timeline) {
        current.timeline += ' ' + line;
      } else if (current.difficulty) {
        current.difficulty += ' ' + line;
      } else if (current.overview) {
        current.overview += ' ' + line;
      } else if (current.name) {
        current.name += ' ' + line;
      }
    }
  });

  if (current.name) structured.push(current as ParsedIdea);
  return structured;
}


export default function IdeasScreen({ route, navigation }: Props) {
  const { formData, retainedIdeas } = route.params;
  const [ideas, setIdeas] = useState<ParsedIdea[] | null>(null);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  useEffect(() => {
    if (retainedIdeas) {
      setIdeas(retainedIdeas);
      return; // Stop here if ideas are retained
    }

    async function fetchIdeas() {
      try {
        const response = await fetch('http://127.0.0.1:8000/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        const rawIdeas = Array.isArray(data.ideas) ? data.ideas : Object.values(data)[0];
        const parsed = parseIdeaBlocks(
          rawIdeas.flatMap((idea: string) => idea.split('\n'))
        );
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

  const handleSelectIdea = (index: number) => {
    setSelectedIndex(index === selectedIndex ? null : index);
  };

  return (
    <ScrollView contentContainerStyle={{ paddingBottom: 100 }} className="bg-white px-5">
      <View className="mt-6">
        <CustomHeader title="Your Project Ideas" showBack />
      </View>

      {ideas.map((idea, index) => (
        <TouchableOpacity
          key={index}
          onPress={() => handleSelectIdea(index)}
          style={{
            marginTop: 16,
            borderRadius: 12,
            borderWidth: 1,
            borderColor: selectedIndex === index ? '#000' : '#e5e7eb',
            backgroundColor: '#fff',
            padding: 16,
            marginBottom: 16,
            shadowColor: '#000',
            shadowOpacity: 0.04,
            shadowRadius: 4,
            shadowOffset: { width: 0, height: 2 },
          }}
        >
          <Text style={{ fontWeight: 'bold', fontSize: 16, color: '#111' }}>{idea.name}</Text>

          <Text style={{ color: '#6b7280', fontSize: 13, marginTop: 10 }}>Overview:</Text>
          <Text style={{ color: '#111', fontSize: 15, marginTop: 2 }}>{idea.overview}</Text>

          <Text style={{ color: '#6b7280', fontSize: 13, marginTop: 10 }}>Difficulty:</Text>
          <Text style={{ color: '#111', fontSize: 15, marginTop: 2 }}>{idea.difficulty}</Text>

          <Text style={{ color: '#6b7280', fontSize: 13, marginTop: 10 }}>Timeline:</Text>
          <Text style={{ color: '#111', fontSize: 15, marginTop: 2 }}>{idea.timeline}</Text>
        </TouchableOpacity>
      ))}

      <View className="mt-6 space-y-3">
        <TouchableOpacity
          disabled={selectedIndex === null}
          className={`py-4 rounded-xl items-center ${
            selectedIndex === null ? 'bg-gray-400' : 'bg-black'
          }`}
          onPress={() => {
            if (selectedIndex !== null) {
              const selected = ideas[selectedIndex];
              console.log('Liked idea:', selected.name);
              // Add future navigation here
            }
          }}
        >
          <Text className="text-white text-base font-bold">I like this idea</Text>
        </TouchableOpacity>

        <TouchableOpacity
          className="py-4 rounded-xl items-center border border-black"
          onPress={() => {
            navigation.navigate("Chat", { previousMessages: [] })
          }}
        >
          <Text className="text-black text-base font-bold">
            Chat with an agent to find an idea for you!
          </Text>
        </TouchableOpacity>


        <TouchableOpacity
          className="mt-4 py-3 rounded-xl items-center bg-gray-100 border border-gray-400"
          onPress={() => navigation.navigate('Form')}
        >
          <Text className="text-gray-700 text-base">← Back to Form</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}
