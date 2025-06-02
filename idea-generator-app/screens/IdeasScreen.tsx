import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
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
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" />
        <Text style={{ marginTop: 20, color: '#555' }}>Generating your ideas...</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <CustomHeader title="Your Project Ideas" showBack />

      {ideas.map((idea, index) => (
        <View key={index} style={styles.ideaCard}>
            <Text style={styles.ideaTitle}>{idea.name}</Text>
            <Text style={styles.ideaLabel}>Overview:</Text>
            <Text style={styles.ideaText}>{idea.overview}</Text>
            <Text style={styles.ideaLabel}>Difficulty:</Text>
            <Text style={styles.ideaText}>{idea.difficulty}</Text>
            <Text style={styles.ideaLabel}>Timeline:</Text>
            <Text style={styles.ideaText}>{idea.timeline}</Text>
        </View>
        ))}


      <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
        <Text style={styles.buttonText}>← Back to Form</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    paddingBottom: 60,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 100,
    backgroundColor: '#fff',
  },
  ideaCard: {
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    borderColor: '#ddd',
    borderWidth: 1,
  },
  button: {
    marginTop: 20,
    backgroundColor: '#000',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  header: {
  fontSize: 26,
  fontFamily: 'Inter-SemiBold',
  marginBottom: 20,
  color: '#000',
},
ideaTitle: {
  fontSize: 18,
  fontFamily: 'Inter-SemiBold',
  marginBottom: 5,
  color: '#000',
},
ideaLabel: {
  fontFamily: 'Inter-Medium',
  marginTop: 10,
  color: '#555',
},
ideaText: {
  fontSize: 16,
  fontFamily: 'Inter',
  color: '#333',
  lineHeight: 22,
},

});
