import React from 'react'
import styled, { keyframes } from 'styled-components'
import { motion } from 'framer-motion'
import tireImage from '../assets/f1_tire.png'

const spin = keyframes`
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
`;

const LoadingWrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 3rem;
`;

const Tire = styled.img`
    width: 100px;
    height: 100px;
    animation: ${spin} 1s linear infinite;
`;

const Message = styled(motion.div)`
    margin-top: 1.5rem;
    font-size: 1.3rem;
    color: white;
`;

const LoadingScreen = () => {
    return (
        <LoadingWrapper>
            <Tire src={tireImage} alt="Spinning F1 tire"/>
            <Message
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 1, repeat: Infinity, repeatType: 'reverse' }}
            >
                Predicting Race Results...
            </Message>
        </LoadingWrapper>
    );
};

export default LoadingScreen;