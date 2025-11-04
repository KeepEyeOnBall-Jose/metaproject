import { Canvas, useFrame } from '@react-three/fiber';
import { Text, Sphere, Float, MeshDistortMaterial } from '@react-three/drei';
import { useRef, useMemo, useState } from 'react';
import * as THREE from 'three';

// Animated floating bubble component
function FloatingBubble({ position, size, category, count, onClick, isSelected }) {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  // Random floating animation
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.5 + position[0]) * 0.3;
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
      meshRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.4) * 0.1;
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
      <group
        ref={meshRef}
        position={position}
        onClick={() => onClick(category)}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        {/* Main bubble sphere */}
        <Sphere args={[size, 32, 32]}>
          <MeshDistortMaterial
            color={isSelected ? "#ff6b6b" : hovered ? "#4ecdc4" : "#74b9ff"}
            transparent
            opacity={0.8}
            distort={0.3}
            speed={2}
            roughness={0.1}
            metalness={0.1}
          />
        </Sphere>

        {/* Inner glow sphere */}
        <Sphere args={[size * 0.8, 16, 16]}>
          <meshBasicMaterial
            color={isSelected ? "#ff4757" : "#00d2d3"}
            transparent
            opacity={0.3}
          />
        </Sphere>

        {/* Category text */}
        <Text
          position={[0, size + 0.3, 0]}
          fontSize={size * 0.3}
          color={isSelected ? "#ff4757" : "#2f3542"}
          anchorX="center"
          anchorY="middle"
        >
          {category}
        </Text>

        {/* Question count */}
        <Text
          position={[0, -size - 0.3, 0]}
          fontSize={size * 0.2}
          color="#57606f"
          anchorX="center"
          anchorY="middle"
        >
          {count}
        </Text>
      </group>
    </Float>
  );
}

function ConceptCloud({ categories, onSelectCategory }) {
  const groupRef = useRef();
  const [selectedCategory, setSelectedCategory] = useState(null);

  // Generate 3D positions using a more natural clustering algorithm
  const bubbleData = useMemo(() => {
    const categoryKeys = Object.keys(categories);
    return categoryKeys.map((category, i) => {
      const count = categories[category];

      // Create clustering effect - similar categories cluster together
      const clusterAngle = (i / categoryKeys.length) * Math.PI * 2;
      const clusterRadius = 2 + Math.sin(i * 0.5) * 1.5;
      const heightVariation = Math.sin(i * 0.7) * 2;

      // Add some randomness for natural distribution
      const randomOffset = {
        x: (Math.random() - 0.5) * 1.5,
        y: (Math.random() - 0.5) * 1.5,
        z: (Math.random() - 0.5) * 1.5,
      };

      return {
        category,
        count,
        position: [
          Math.cos(clusterAngle) * clusterRadius + randomOffset.x,
          heightVariation + randomOffset.y,
          Math.sin(clusterAngle) * clusterRadius + randomOffset.z,
        ],
        size: Math.max(0.3, Math.min(1.2, count * 0.08 + 0.4)), // Size based on count
      };
    });
  }, [categories]);

  const handleBubbleClick = (category) => {
    const newSelected = selectedCategory === category ? null : category;
    setSelectedCategory(newSelected);
    onSelectCategory(newSelected);
  };

  return (
    <div style={{ width: '100%', height: '500px', position: 'relative' }}>
      <Canvas
        camera={{ position: [0, 0, 8], fov: 60 }}
        frameloop="demand"
        style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
      >
        {/* Lighting setup */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <pointLight position={[-10, -10, -5]} intensity={0.5} color="#ff6b6b" />

        {/* Environment and effects */}
        <fog attach="fog" args={['#f0f0f0', 8, 15]} />

        <group ref={groupRef}>
          {/* Render bubbles */}
          {bubbleData.map((bubble, i) => (
            <FloatingBubble
              key={bubble.category}
              position={bubble.position}
              size={bubble.size}
              category={bubble.category}
              count={bubble.count}
              onClick={handleBubbleClick}
              isSelected={selectedCategory === bubble.category}
            />
          ))}
        </group>
      </Canvas>

      {/* UI Overlay */}
      <div style={{
        position: 'absolute',
        top: '10px',
        left: '10px',
        background: 'rgba(255, 255, 255, 0.9)',
        padding: '10px',
        borderRadius: '8px',
        fontSize: '14px',
        color: '#333'
      }}>
        <div><strong>3D Concept Cloud</strong></div>
        <div>Categories: {Object.keys(categories).length}</div>
        <div>Total Questions: {Object.values(categories).reduce((a, b) => a + b, 0)}</div>
        {selectedCategory && (
          <div style={{ color: '#ff4757', marginTop: '5px' }}>
            Selected: {selectedCategory} ({categories[selectedCategory]} questions)
          </div>
        )}
      </div>
    </div>
  );
}

export default ConceptCloud;