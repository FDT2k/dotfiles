zmodload zsh/zprof
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH
export NVM_LAZY=1
# Path to your oh-my-zsh installation.
export ZSH="/home/fabien/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="fdt2k"

export FZF_DEFAULT_OPTS="--border=bold --margin=1%"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)
source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias pbpaste='xclip -selection clipboard -o'
alias sail='bash vendor/bin/sail'
alias sartisan='sail artisan'
alias artisan='php artisan'
alias dockersail='docker-compose -f docker/docker-compose.yml exec myapp'

alias php8.2="docker run --rm --interactive --tty  --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2 php"
alias composer2-php8.2-prod="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app -w /app --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2  composer2"
alias composer2-php8.1-prod="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.1  composer2"
alias composer2-php8.2="docker run --rm --interactive --tty  --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2 composer2"
alias composer2-php8.2-dev="docker run --rm --interactive --tty -e COMPOSER=composer.dev.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2  composer2"
alias php-8.2="docker run --rm --interactive --tty --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) -w /app registry.gitlab.com/karsegard/docker-infomaniak:8.2 php"
alias php-8.1="docker run --rm --interactive --tty --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.1 php"
alias php-8.2-shell="docker run --rm --interactive --tty --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2 bash"

alias php-8.4="docker run --rm --interactive --tty --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.4 php"
alias composer2-php8.4-dev="docker run --rm --interactive --tty -e COMPOSER=composer.dev.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.4  composer2"
alias composer2-php8.4-prod="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(pwd)"/../..,target=/monorepo,readonly     --mount type=bind,source="$(pwd)",target=/app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.4  composer2"

alias config='/usr/bin/git --git-dir=$HOME/dotfiles/ --work-tree=$HOME'
compdef config=git
config config --local status.showUntrackedFiles no

alias chromium-w='chromium --enable-features=UseOzonePlatform --ozone-platform=wayland'

source ~/init-php-aliases.sh

#alias gitsmtags="for i in $(git config --file .gitmodules --get-regexp path | awk '{ print $2 }'); do echo $i\":\"; git push --tags ; done"
#export NVM_DIR="$HOME/.nvm"
#[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

source /usr/share/nvm/init-nvm.sh



export PATH=$PATH:$HOME/.yarn/bin:$HOME/.cargo/bin:$HOME/bin
export PATH=$PATH:$HOME/.config/composer/vendor/bin
export PATH=$PATH:/var/lib/flatpak/exports/bin
export NODE_OPTIONS=--max_old_space_size=30000
#apply color theme
wal --vte -Rq
EDITOR=ox
source $HOME/.shell-keys/keys
source <(fzf --zsh)
export PATH="$HOME/.local/bin:$PATH"
