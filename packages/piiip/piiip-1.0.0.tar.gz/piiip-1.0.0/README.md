# piiip - piiip interactively installs intended packages

piiip (Piiip Interactively Installs Intended Packages) is a wrapper around pip that helps to
avoid installation of a different package than was intended. For example, when
executing `piiip install pandaa` (panda**a** instead of panda**s**), piiip asks
for a confirmation before commencing the installation of pandaa. Accidentally
installing a different package than was intended can result in security risks,
including attackers getting control over the machine on which the unintended
package is installed[^3]. piiip is a drop-in replacement for pip; usage is
exactly equal.

## What can go wrong?

Using pip, it is trivial to install any desired package from PyPI by just
specifying the desired package name. If the package name is incorrect however,
for example due to a typo, a different package is installed than was intended.
This package might contain outdated, vulnerable or even outright malicious
software, which can result in a compromised machine (see [^3]) for an overview
when and how packages can do arbitrary code execution). Malicious parties are
actively uploading malicious packages to compromise systems, similar to domain
typosquatting attacks. These packages, which have a name that is designed to be
confused with a legitimate package name, are used to steal information, private
keys or install backdoors on target machines[^10].

### Does this actually go wrong in practice?

Yes. Several projects to protect users of pip have registered dummy packages
with names that can be easily confused with popular packages. By claiming these
names, real attackers cannot use the names for typosquatting purposes anymore.
This is called "defensive typosquatting". Two defensive typosquatting projects
[^8] [^9] received more than a million downloads in total on their packages,
showing how often a typo happens. Furthermore, a student was able to run code on
17,000 unique hosts only 7 weeks after uploading 200 packages with a name that
could be easily confused with popular packages[^7]. The Advanced Persistent
Threat (APT) Lazarus also employed the package name confusion technique[^6].
Other groups have also attracted attention by using package name confusion
techniques to steal
[source code](https://blog.phylum.io/targeted-npm-malware-attempts-to-steal-developers-source-code-and-secrets/),
[cryptocurrency](https://medium.com/@bertusk/cryptocurrency-clipboard-hijacker-discovered-in-pypi-repository-b66b8a534a8),
[SSH and GPG keys](https://www.zdnet.com/article/two-malicious-python-libraries-removed-from-pypi/),
[credentials](https://threatpost.com/attackers-use-typo-squatting-to-steal-npm-credentials/127235/)
and
[Discord tokens](https://bertusk.medium.com/discord-token-stealer-discovered-in-pypi-repository-e65ed9c3de06).

### Package name confusion and typosquatting

The term "package name confusion" is used to describe all ways in which a user
can install a different package than intended. The most intuitive example of
package name confusion is a typing error (typosquatting: pand**d**as instead of
pandas). Other causes include a different spelling (colourama instead of
colorama), delimiter modification (charsetnormalizer instead of
charset-normalizer), prefix/suffix augmentation (py-pandas instead of pandas).
Neupane et al. created an overview of package name confusion categories[^1].

## How does piiip help?

piiip adds a layer of safety by asking confirmation before installing packages.
It only asks for confirmation if a package name might not represent the package
that was intended to be installed. This way, piiip is not a burden on the user,
but can prevent security issues. For example, when running `piiip install pandas`
the behavior of piiip is identical to pip. But when running
`piiip install pandaa`, piiip asks:

> A package named pandas instead of pandaa exists. Are you sure you want to
> install pandaa? (y/n)

Examples of real malicious packages that would have triggered a warning by piiip
are:

| Malicious package name | Real package name | Category according to [^1]          | Source                                                                                                                      |
| ---------------------- | ----------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| python3-dateutil       | dateutil          | Prefix/suffix augmentation          | [Snyk](https://snyk.io/blog/malicious-packages-found-to-be-typo-squatting-in-pypi/)                                         |
| urlib3                 | urllib3           | 1-step Damerau/Levenshtein distance | [IQT](https://web.archive.org/web/20240303213334/https://www.iqt.org/bewear-python-typosquatting-is-about-more-than-typos/) |
| colourama              | colorama          | Alternate spelling                  | [Neupane et al.](https://www.usenix.org/system/files/usenixsecurity23-neupane.pdf)                                          |

### Usage

piiip is fully compatible with PIP. You can use `piiip` in the exact same manner
as `pip` (or `pip3`) and you won't see any difference until a possible name
confusion occurs. In that case, piiip will ask you to confirm the installation of
the package. Note that packages installed with the option `--index-url` are
**not** analyzed for name confusion.

For example, if you want to install `pandas` you run:

```console
piiip install pandas
```

For more information, run

```console
piiip --help
```

![piiip demo](https://raw.githubusercontent.com/TNO-S3/piiip/main/assets/piiip_demo.gif)

## Features

piiip currently detects the following categories[^1] of package name confusion:

| Category                       | Protects against:                                            | Example                   |
| ------------------------------ | ------------------------------------------------------------ | ------------------------- |
| Character omission             | Forgetting a character in the package name                   | panda                     |
| Character addition             | Adding an additional character in the package name           | pand**d**as               |
| Swapped character              | Changing the location of two characters                      | pan**ad**s                |
| Substituted character          | Exchanging a character for a random other character          | pan**f**as                |
| Prefix/suffix augmentation[^2] | Adding a keyword before or after the package name            | pandas-**py**             |
| Alternate spelling             | Exchanging a British word for an American word or vice versa | colorama -> colo**u**rama |
| Homographic replacement        | Exchanging one or more characters that look alike            | colorama -> col0rama      |

Note that only one mistake can be made in the package name. Packages with two
mistakes, or mistakes from two categories are not detected. Examples of what is
not detected: panddas-py, pandddas and pndass.

## Installing piiip

Method 1:

1. Clone the repository
2. Run `python -m pip install .`

Method 2:

Run `pip install piiip`.

## Roadmap

- Add detection methods for other categories[^1] of package name confusion:
  - Sequence reordering
  - Grammatical substitution
  - Semantic substitution
  - Asemantic substitution
  - Homophonic similarity
  - Simplification
- Implement a more robust method to determine package popularity

## How does piiip work?

piiip performs two main tasks when it receives a package name:

1. Generating alternative package names that the user might have intended
   instead of the received package name
2. Determining the popularity of all packages alternative package names and the
   received package

If one of the alternative package names belong to a package that is more popular
than the received package name, the warning is shown. The generation of
alternative package names is performed for the categories listed under
**Features**. Popularity of packages is currently determined by using download
statistics from [pypistats.org](https://pypistats.org/).

## Alternatives for other online package repositories

piiip only works for pip. For npm, TypoGard[^5] by Taylor et al. can be used.
TypoGard has the same goal as piiip and has been integrated in (a specific
version of) the npm package installer[^4].

[^1]:
    the listed categories are taken from
    ["Beyond Typosquatting: An In-depth Look at Package Confusion" by Neupane et al.](https://www.usenix.org/system/files/usenixsecurity23-neupane.pdf)

[^2]: for a very limited set of prefixes/suffixes

[^3]: https://arxiv.org/pdf/2307.09087

[^4]: https://github.com/mt3443/typogard

[^5]: https://ldklab.github.io/assets/papers/nss20-typogard.pdf

[^6]: https://blogs.jpcert.or.jp/en/2024/02/lazarus_pypi.html

[^7]: https://incolumitas.com/data/thesis.pdf

[^8]: https://medium.com/@williambengtson/python-typosquatting-for-fun-not-profit-99869579c35d

[^9]: https://hackernoon.com/building-a-botnet-on-pypi-be1ad280b8d6

[^10]: https://arxiv.org/pdf/2309.11021
