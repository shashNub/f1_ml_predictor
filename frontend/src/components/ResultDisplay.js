import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import carIcon from '../assets/f1_car.png';
import PodiumDisplay from './PodiumDisplay';

const ResultContainer = styled.div`
  margin-top: 40px;
  text-align: center;
`;

const ResultRow = styled(motion.div)`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  font-size: 1.5rem;
`;

const CarIcon = styled.img`
  width: 80px;
  height: auto;
  margin-right: 12px;
`;

const SectionTitle = styled(motion.h3)`
  margin-top: 2rem;
  font-size: 1.8rem;
`;

const resultVariants = {
  hidden: { x: '-100vw', opacity: 0 },
  visible: (i) => ({
    x: 0,
    opacity: 1,
    transition: {
      delay: i * 0.5,
      type: 'spring',
      stiffness: 50,
    },
  }),
};

const sectionTitleVariants = {
  hidden: { opacity: 0, y: -20 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.4,
      duration: 0.6,
      type: 'spring',
    },
  }),
};

const getMedal = (index) => {
  const medals = ['🥇', '🥈', '🥉', '🏅', '🎖️'];
  return medals[index] || '';
};

// removed unused Spacer to satisfy eslint in CI

const ResultDisplay = ({ predictions, error }) => {
  if (error) {
    return (
      <ResultContainer>
        <p style={{ color: 'red' }}>{error}</p>
      </ResultContainer>
    );
  }

  if (!predictions || predictions.length === 0) return null;

  const podium = predictions.slice(0, 3);
  const others = predictions.slice(3, 5);

  return (
    <ResultContainer>
      <motion.h2
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        🏁 Predicted Top Finishers
      </motion.h2>
      <PodiumDisplay predictions={podium} />

      {/* 4th and 5th Place */}
      {others.length > 0 && (
        <>
          <SectionTitle
            custom={1}
            initial="hidden"
            animate="visible"
            variants={sectionTitleVariants}
          >
            🏁 Other Top Finishers
          </SectionTitle>
          {others.map((entry, index) => (
            <ResultRow
              key={index + 3}
              custom={index}
              initial="hidden"
              animate="visible"
              variants={resultVariants}
            >
              <CarIcon src={carIcon} alt="F1 Car" />
              <span>
                {getMedal(index + 3)} {entry.driver} ({entry.constructor})
              </span>
            </ResultRow>
          ))}
        </>
      )}
    </ResultContainer>
  );
};

export default ResultDisplay;
