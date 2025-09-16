import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import trophyIcon from '../assets/trophy.png';
import tireBase from '../assets/f1_tire.png';

import driver1 from '../assets/drivers/driver1.png';
import driver2 from '../assets/drivers/driver2.png';
import driver3 from '../assets/drivers/driver3.png';

const PodiumSection = styled.section`
  padding: 60px 20px 100px;
  min-height: 700px;
  position: relative;
  color: #fff;
`;


const SectionTitle = styled(motion.h2)`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 40px;
`;

const PodiumWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 60px;
  margin-top: 120px;
  position: relative;
  z-index: 2;
`;

const PodiumBlock = styled(motion.div)`
  width: 160px;
  background: ${({ color }) => color};
  border-radius: 16px 16px 0 0;
  text-align: center;
  position: relative;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.6);
  padding-top: 50px;

  &.first { height: 260px; }
  &.second { height: 200px; }
  &.third { height: 180px; }
`;

const DriverAvatar = styled.img`
  width: 120px;
  height: 200px;
  position: absolute;
  top: -180px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
  background: #111;
  z-index: 3;
`;

const DriverName = styled.p`
  font-weight: bold;
  font-size: 1.5rem;
  margin-top: 10px;
`;

const TeamName = styled.p`
  font-size: 0.95rem;
`;

const TireImage = styled.img`
  position: absolute;
  width: 90px;
  bottom: -55px;
  left: 50%;
  transform: translateX(-50%);
`;

const Trophy = styled.img`
  position: absolute;
  bottom: -320px;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  z-index: 1;
`;

const Spacer = styled.div`
  height: 120px;
`;

const PodiumDisplay = ({ predictions }) => {
  const colors = ['#C0C0C0', '#FFD700', '#CD7F32']; // silver, gold, bronze
  const avatars = [driver2, driver1, driver3]; // 2nd, 1st, 3rd
  const positions = ['second', 'first', 'third'];
  const transition = { duration: 0.6, type: 'spring' };

  return (
    <PodiumSection>
      <SectionTitle
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={transition}
      >
      </SectionTitle>

      <PodiumWrapper>
        {predictions.slice(0, 3).map((driver, i) => (
          <PodiumBlock
            key={driver.driver}
            className={positions[i]}
            color={colors[i]}
            initial={{ scale: 0, y: 100 }}
            animate={{ scale: 1, y: 0 }}
            transition={{ delay: i * 0.2, ...transition }}
          >
            <DriverAvatar src={avatars[i]} alt={`Driver ${i + 1}`} />
            <DriverName>{driver.driver}</DriverName>
            <TeamName>{driver.constructor}</TeamName>
            <TireImage src={tireBase} alt="Tire base" />
            {i === 1 && <Trophy src={trophyIcon} alt="Trophy" />}
          </PodiumBlock>
        ))}
      </PodiumWrapper>

      <Spacer />
    </PodiumSection>
  );
};

export default PodiumDisplay;
