import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

export default function CongratsScreen({ navigation, route }: any) {
  const selectedIdea = route.params?.selectedIdea;
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: 'white', padding: 24 }}>
      <Text style={{ fontSize: 28, fontWeight: 'bold', marginBottom: 24, fontFamily: 'Klados-Bold', textAlign: 'center' }}>
        🎉 CONGRATS ON PICKING AN IDEA
      </Text>
      {selectedIdea && (
        <View style={{ backgroundColor: '#f3f3f3', borderRadius: 10, padding: 16, marginBottom: 24, width: '100%' }}>
          <Text style={{ fontFamily: 'Klados-Bold', fontSize: 18, color: '#222', textAlign: 'center', marginBottom: 8 }}>{selectedIdea.name}</Text>
          {selectedIdea.skills && (
            <>
              <Text style={{ fontFamily: 'Klados-Bold', fontSize: 14, color: '#444', marginBottom: 4 }}>Project Skills:</Text>
              <Text style={{ fontSize: 14, color: '#222', marginBottom: 8 }}>{selectedIdea.skills.replace(/^Project\s+/i, '')}</Text>
            </>
          )}
          <Text style={{ fontFamily: 'Klados-Bold', fontSize: 14, color: '#444', marginBottom: 4 }}>Overview:</Text>
          <Text style={{ fontSize: 14, color: '#222', marginBottom: 8 }}>{selectedIdea.overview}</Text>
          <Text style={{ fontFamily: 'Klados-Bold', fontSize: 14, color: '#444', marginBottom: 4 }}>Difficulty:</Text>
          <Text style={{ fontSize: 14, color: '#222', marginBottom: 8 }}>{selectedIdea.difficulty}</Text>
          <Text style={{ fontFamily: 'Klados-Bold', fontSize: 14, color: '#444', marginBottom: 4 }}>Timeline:</Text>
          <Text style={{ fontSize: 14, color: '#222' }}>{selectedIdea.timeline}</Text>
        </View>
      )}
      <TouchableOpacity
        style={{ backgroundColor: 'black', paddingVertical: 16, paddingHorizontal: 32, borderRadius: 10, marginTop: 24 }}
        onPress={() => navigation.navigate('Dashboard', { selectedIdea })}
      >
        <Text style={{ color: 'white', fontSize: 18, fontFamily: 'Klados-Bold' }}>Back to Dashboard</Text>
      </TouchableOpacity>
    </View>
  );
} 