import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, FlatList } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function ProjectDashboard() {
  const navigation = useNavigation<NavigationProp>();
  const [projects, setProjects] = useState<any[]>([]); // Future: replace 'any' with a proper type

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Projects</Text>

      {projects.length === 0 ? (
        <Text style={styles.emptyText}>No projects yet. Create your first one!</Text>
      ) : (
        <FlatList
          data={projects}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.projectCard}>
              <Text>{item.name}</Text>
            </View>
          )}
        />
      )}

      <TouchableOpacity
        style={styles.createButton}
        onPress={() => navigation.navigate('Form')}
      >
        <Text style={styles.buttonText}>+ Create New Project</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.logoutButton}
        onPress={() => navigation.navigate('HomeLogin')}
      >
        <Text style={styles.logoutText}>Log Out</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#000',
  },
  emptyText: {
    fontSize: 16,
    color: '#777',
    marginBottom: 32,
    textAlign: 'center',
  },
  projectCard: {
    padding: 16,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    marginBottom: 12,
    width: '100%',
  },
  createButton: {
    backgroundColor: '#000',
    paddingVertical: 14,
    paddingHorizontal: 40,
    borderRadius: 12,
    marginTop: 24,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  logoutButton: {
    marginTop: 20,
  },
  logoutText: {
    color: '#888',
    fontSize: 14,
    textDecorationLine: 'underline',
  },
});