from setuptools import setup

package_name = "p.e.a.c.e_f.o.r_g.a.z.a".replace(".", "")

url = "https://github.com/peace-and-love-py/peace_for_g#a#z#a".replace("#", "")

README = """
# PEACE FOR G.A.Z.A

## For what?

- To remember the catastrophic situation in the M.iddle E.ast 
- To apply international law, for every countries
- To find a peace solution, sustainable
- To judge all crimes about innocent people
- To counter the lack of transparency and neutrality of the Western media
- To not stigmatise people: people != government

## How can you help?

- Include in python projects, (requirements and optionally import peace function)
- Create other project like this
- Communicate about the situation


## Note

Soon, this account will be b.a.n.n.e.d. 
"""

setup(
    name=package_name,
    long_description=README,
    long_description_content_type='text/markdown',
    url=url,
    version='0.1',
    install_requires=[],
    entry_points={
        'console_scripts': [
            f'peace = {package_name}.{package_name}:_main',
        ]
    }
)
