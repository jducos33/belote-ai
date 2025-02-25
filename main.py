# main.py
import argparse
from belote_env import BeloteEnv

def run_episode(env):
    """Exécute un épisode complet dans l'environnement et retourne le nombre de steps et la récompense totale."""
    obs = env.reset()
    done = False
    total_reward = 0
    step_count = 0

    while not done:
        # Ici, l'action est choisie aléatoirement (pour tester)
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        total_reward += reward
        step_count += 1
        env.render()

    return step_count, total_reward

def main():
    parser = argparse.ArgumentParser(description="Exécution de l'environnement Belote pour du RL")
    parser.add_argument("--episodes", type=int, default=1, help="Nombre d'épisodes à exécuter")
    args = parser.parse_args()

    env = BeloteEnv()
    total_steps = 0
    total_rewards = 0

    for ep in range(args.episodes):
        print(f"\n=== Début de l'épisode {ep+1} ===")
        steps, reward = run_episode(env)
        print(f"Épisode {ep+1} terminé après {steps} steps, récompense totale: {reward:.2f}")
        total_steps += steps
        total_rewards += reward

    print(f"\nStatistiques sur {args.episodes} épisodes :")
    print(f"  Steps moyens  : {total_steps / args.episodes:.2f}")
    print(f"  Récompense moyenne : {total_rewards / args.episodes:.2f}")

if __name__ == '__main__':
    main()
