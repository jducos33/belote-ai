# train.py
import gym
from stable_baselines3 import PPO  # On importe PPO au lieu de DQN
from stable_baselines3.common.evaluation import evaluate_policy

from belote_env import BeloteEnv

def main():
    # Création de l'environnement
    env = BeloteEnv(controlled_agent_id=1, draft_starting_index=0)
    
    # Instanciation du modèle PPO avec une politique MLP
    model = PPO("MlpPolicy", env, verbose=1)
    
    # Entraînement du modèle pendant, par exemple, 100000 timesteps
    model.learn(total_timesteps=100000)
    
    # Évaluation du modèle sur 10 épisodes
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Récompense moyenne: {mean_reward:.2f} +/- {std_reward:.2f}")
    
    # Sauvegarde du modèle entraîné
    model.save("ppo_belote_model")
    
    # Test interactif du modèle
    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        env.render()

if __name__ == '__main__':
    main()
