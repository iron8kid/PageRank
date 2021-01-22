import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked=corpus[page]
    dic =dict()
    if(len(linked)):
        p0 =(1-damping_factor)/len(corpus)
        p1=damping_factor/len(linked)
        for elt in corpus.keys():
            dic[elt]=p0
            if elt in linked:
                dic[elt]+=p1
    else:
        p0=1/len(corpus)
        for elt in corpus.keys():
            dic[elt]=p0
    return dic

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank={ page:0 for page in corpus.keys()}
    prevpage=random.choice(list(corpus.keys()))
    rank[prevpage]+=1
    for i in range(n-1):
        dic=transition_model(corpus,prevpage,damping_factor)
        page=random.choices(list(dic.keys()),list(dic.values()))[0]
        rank[page]+=1
        prevpage=page
    for page in rank.keys():
        rank[page]/=n
    return rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dic=dict()
    N= len(corpus.keys())
    for l in corpus.keys():
        dic[l]=1/N
    while True:
        ok=False
        for page in corpus.keys():
            linked=list()
            old=dic[page]
            for elt in corpus.keys():
                if page in corpus[elt]:
                    linked.append(elt)
            if len(linked):
                dic[page]=(1-damping_factor)/N
                for elt in linked:
                    dic[page]+= damping_factor*dic[elt]/len(corpus[elt])
            ok=((old-dic[page])<0.001 ) and ((old-dic[page])>-0.001 )

        if ok:
            break
    return dic



if __name__ == "__main__":
    main()
