import random
from typing import Literal

import aiohttp

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """Gets a Random Leet Code Problem"""

    name = "leetcode"
    description = (
        "info: find total number of problem, gen: generate a new leetcode problem"
    )
    # discord command descriptions must be less than 100 characters long
    # description = "Generates a random leetcode problem, use info to find total number of problem, use gen to generate a new problem"

    async def execute(self, interaction, command: Literal["info", "gen"]) -> None:
        leet_code_api_url = "https://leetcode.com/api/problems/all"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(leet_code_api_url) as resp:
                problem_data = await resp.json()
        total_problem = problem_data["num_total"]

        if command == "info":
            embed = Embed(
                title="Leet Code Problem",
                description=f"Total number of problems generated : {total_problem}.\nRun `/leetcode gen` to generate random problem. Happy Coding :))",
            )
            await interaction.response.send_message(embed=embed)

        elif command == "gen":
            # Picks a random number betwwn 0 and total number of problem in leetcode - 1
            problem_index = random.randint(0, total_problem - 1)

            # Picks a random problem from all problems in leetcode
            problem = problem_data["stat_status_pairs"][problem_index]

            # Generates problem id
            problem_id = problem["stat"]["question_id"]

            # Generated problem title
            problem_title = problem["stat"]["question__title"]

            # Specify if the problem is paid or free
            problem_access = problem["paid_only"]
            problem_status = None
            if problem_access:
                problem_status = "Paid"
            else:
                problem_status = "Free"

            # Specify the diffculty of the problem
            problem_difficulty_level = problem["difficulty"]["level"]
            problem_difficulty = None
            if problem_difficulty_level == 1:
                problem_difficulty = "Easy"
            elif problem_difficulty_level == 2:
                problem_difficulty = "Moderate"
            else:
                problem_difficulty = "Hard"

            # Creates the Leetcode URL
            problem_url = (
                "https://leetcode.com/problems/"
                + problem["stat"]["question__title_slug"]
                + "/"
            )

            embed = Embed(
                title=problem_title,
                description=f"Problem ID: {problem_id}\n\nProblem Details: {problem_url}\n\nProblem Status: {problem_status}\n\nProblem Difficulty : {problem_difficulty}",
            )

            await interaction.response.send_message(embed=embed)

        else:
            raise KeyError(f"Command {command} not found.")
