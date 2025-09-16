import React from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { motion } from 'framer-motion';

const PanelWrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
`;
const Title = styled.h1 `
    font-size: 3rem;
    font-weight: bold;
    color: #ff0000;
    text-shadow: 2px 2px #222;
    margin-bottom: 2rem;
`;
const Input = styled.input `
    padding: 1rem;
    font-size: 1.2rem;
    width: 300px;
    border: 2px solid #ccc;
    border-radius: 8px;
    margin-bottom: 1rem;
    background-color: #222;
    color: white;
`;
const Button = styled(motion.button) `
    padding: 0.8rem 1.5rem;
    font-size: 1.2rem;
    background: #e10600;
    border: none;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    transition: background 0.3 ease;

    &:hover {
        background: #b20000;
    }
`;

// removed unused ErrorMsg to satisfy eslint in CI

const PredictorPanel = ({ prixName, setPrixName, setPredictions, setIsLoading, setError }) => {
    const handlePredict = async () => {
        if (!prixName.trim()) {
            setError("Please Enter a Valid Prix Name.");
            return;
        }

        setIsLoading(true);
        setError('');
        setPredictions([]);

        try {
            const baseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
            const apiUrl = baseUrl.endsWith('/') ? `${baseUrl}predict` : `${baseUrl}/predict`;
            const response = await axios.post(apiUrl, {
                prix: prixName.toLowerCase().trim(),

            });
            setPredictions(response.data.predictions);
        } catch (err) {
            setError("Prediction failed. Please check Prix Name or try again later.");
        } finally {
            setIsLoading(false)
        }

    };

    return(
        <PanelWrapper>
            <Title>🏁 F1 Race Predictor</Title>
            <Input 
                type="text"
                placeholder="Enter the Grand Prix Name"
                value={prixName}
                onChange={(e) => setPrixName(e.target.value)}
            />
            <Button 
                whileTap={{ scale: 0.9 }}
                whileHover={{ scale: 1.05 }}
                onClick={handlePredict}
            >
                Predict
            </Button>
        </PanelWrapper>
    );
};

export default PredictorPanel;